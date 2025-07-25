import asyncio
import logging
import warnings
from functools import partial, update_wrapper
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from aiosignal import Signal
from frozenlist import FrozenList

from . import hdrs
from .abc import (
    AbstractAccessLogger,
    AbstractMatchInfo,
    AbstractRouter,
    AbstractStreamWriter,
)
from .helpers import DEBUG
from .http_parser import RawRequestMessage
from .log import web_logger
from .streams import StreamReader
from .web_log import AccessLogger
from .web_middlewares import _fix_request_current_app
from .web_protocol import RequestHandler
from .web_request import Request
from .web_response import StreamResponse
from .web_routedef import AbstractRouteDef
from .web_server import Server
from .web_urldispatcher import (
    AbstractResource,
    AbstractRoute,
    Domain,
    MaskDomain,
    MatchedSubAppResource,
    PrefixedSubAppResource,
    UrlDispatcher,
)

__all__ = ("Application", "CleanupError")


if TYPE_CHECKING:  
    from .typedefs import Handler

    _AppSignal = Signal[Callable[["Application"], Awaitable[None]]]
    _RespPrepareSignal = Signal[Callable[[Request, StreamResponse], Awaitable[None]]]
    _Middleware = Union[
        Callable[[Request, Handler], Awaitable[StreamResponse]],
        Callable[["Application", Handler], Awaitable[Handler]],  
    ]
    _Middlewares = FrozenList[_Middleware]
    _MiddlewaresHandlers = Optional[Sequence[Tuple[_Middleware, bool]]]
    _Subapps = List["Application"]
else:
    
    _AppSignal = Signal
    _RespPrepareSignal = Signal
    _Middleware = Callable
    _Middlewares = FrozenList
    _MiddlewaresHandlers = Optional[Sequence]
    _Subapps = List


class Application(MutableMapping[str, Any]):
    ATTRS = frozenset(
        [
            "logger",
            "_debug",
            "_router",
            "_loop",
            "_handler_args",
            "_middlewares",
            "_middlewares_handlers",
            "_run_middlewares",
            "_state",
            "_frozen",
            "_pre_frozen",
            "_subapps",
            "_on_response_prepare",
            "_on_startup",
            "_on_shutdown",
            "_on_cleanup",
            "_client_max_size",
            "_cleanup_ctx",
        ]
    )

    def __init__(
        self,
        *,
        logger: logging.Logger = web_logger,
        router: Optional[UrlDispatcher] = None,
        middlewares: Iterable[_Middleware] = (),
        handler_args: Optional[Mapping[str, Any]] = None,
        client_max_size: int = 1024 ** 2,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        debug: Any = ...,  
    ) -> None:
        if router is None:
            router = UrlDispatcher()
        else:
            warnings.warn(
                "router argument is deprecated", DeprecationWarning, stacklevel=2
            )
        assert isinstance(router, AbstractRouter), router

        if loop is not None:
            warnings.warn(
                "loop argument is deprecated", DeprecationWarning, stacklevel=2
            )

        if debug is not ...:
            warnings.warn(
                "debug argument is deprecated", DeprecationWarning, stacklevel=2
            )
        self._debug = debug
        self._router = router  
        self._loop = loop
        self._handler_args = handler_args
        self.logger = logger

        self._middlewares = FrozenList(middlewares)  

        
        self._middlewares_handlers = None  
        
        self._run_middlewares = None  

        self._state = {}  
        self._frozen = False
        self._pre_frozen = False
        self._subapps = []  

        self._on_response_prepare = Signal(self)  
        self._on_startup = Signal(self)  
        self._on_shutdown = Signal(self)  
        self._on_cleanup = Signal(self)  
        self._cleanup_ctx = CleanupContext()
        self._on_startup.append(self._cleanup_ctx._on_startup)
        self._on_cleanup.append(self._cleanup_ctx._on_cleanup)
        self._client_max_size = client_max_size

    def __init_subclass__(cls: Type["Application"]) -> None:
        warnings.warn(
            "Inheritance class {} from web.Application "
            "is discouraged".format(cls.__name__),
            DeprecationWarning,
            stacklevel=2,
        )

    if DEBUG:  

        def __setattr__(self, name: str, val: Any) -> None:
            if name not in self.ATTRS:
                warnings.warn(
                    "Setting custom web.Application.{} attribute "
                    "is discouraged".format(name),
                    DeprecationWarning,
                    stacklevel=2,
                )
            super().__setattr__(name, val)

    

    def __eq__(self, other: object) -> bool:
        return self is other

    def __getitem__(self, key: str) -> Any:
        return self._state[key]

    def _check_frozen(self) -> None:
        if self._frozen:
            warnings.warn(
                "Changing state of started or joined " "application is deprecated",
                DeprecationWarning,
                stacklevel=3,
            )

    def __setitem__(self, key: str, value: Any) -> None:
        self._check_frozen()
        self._state[key] = value

    def __delitem__(self, key: str) -> None:
        self._check_frozen()
        del self._state[key]

    def __len__(self) -> int:
        return len(self._state)

    def __iter__(self) -> Iterator[str]:
        return iter(self._state)

    
    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        
        
        
        warnings.warn("loop property is deprecated", DeprecationWarning, stacklevel=2)
        return cast(asyncio.AbstractEventLoop, self._loop)

    def _set_loop(self, loop: Optional[asyncio.AbstractEventLoop]) -> None:
        if loop is None:
            loop = asyncio.get_event_loop()
        if self._loop is not None and self._loop is not loop:
            raise RuntimeError(
                "web.Application instance initialized with different loop"
            )

        self._loop = loop

        
        if self._debug is ...:
            self._debug = loop.get_debug()

        
        for subapp in self._subapps:
            subapp._set_loop(loop)

    @property
    def pre_frozen(self) -> bool:
        return self._pre_frozen

    def pre_freeze(self) -> None:
        if self._pre_frozen:
            return

        self._pre_frozen = True
        self._middlewares.freeze()
        self._router.freeze()
        self._on_response_prepare.freeze()
        self._cleanup_ctx.freeze()
        self._on_startup.freeze()
        self._on_shutdown.freeze()
        self._on_cleanup.freeze()
        self._middlewares_handlers = tuple(self._prepare_middleware())

        
        
        
        
        
        self._run_middlewares = True if self.middlewares else False

        for subapp in self._subapps:
            subapp.pre_freeze()
            self._run_middlewares = self._run_middlewares or subapp._run_middlewares

    @property
    def frozen(self) -> bool:
        return self._frozen

    def freeze(self) -> None:
        if self._frozen:
            return

        self.pre_freeze()
        self._frozen = True
        for subapp in self._subapps:
            subapp.freeze()

    @property
    def debug(self) -> bool:
        warnings.warn("debug property is deprecated", DeprecationWarning, stacklevel=2)
        return self._debug  

    def _reg_subapp_signals(self, subapp: "Application") -> None:
        def reg_handler(signame: str) -> None:
            subsig = getattr(subapp, signame)

            async def handler(app: "Application") -> None:
                await subsig.send(subapp)

            appsig = getattr(self, signame)
            appsig.append(handler)

        reg_handler("on_startup")
        reg_handler("on_shutdown")
        reg_handler("on_cleanup")

    def add_subapp(self, prefix: str, subapp: "Application") -> AbstractResource:
        if not isinstance(prefix, str):
            raise TypeError("Prefix must be str")
        prefix = prefix.rstrip("/")
        if not prefix:
            raise ValueError("Prefix cannot be empty")
        factory = partial(PrefixedSubAppResource, prefix, subapp)
        return self._add_subapp(factory, subapp)

    def _add_subapp(
        self, resource_factory: Callable[[], AbstractResource], subapp: "Application"
    ) -> AbstractResource:
        if self.frozen:
            raise RuntimeError("Cannot add sub application to frozen application")
        if subapp.frozen:
            raise RuntimeError("Cannot add frozen application")
        resource = resource_factory()
        self.router.register_resource(resource)
        self._reg_subapp_signals(subapp)
        self._subapps.append(subapp)
        subapp.pre_freeze()
        if self._loop is not None:
            subapp._set_loop(self._loop)
        return resource

    def add_domain(self, domain: str, subapp: "Application") -> AbstractResource:
        if not isinstance(domain, str):
            raise TypeError("Domain must be str")
        elif "*" in domain:
            rule = MaskDomain(domain)  
        else:
            rule = Domain(domain)
        factory = partial(MatchedSubAppResource, rule, subapp)
        return self._add_subapp(factory, subapp)

    def add_routes(self, routes: Iterable[AbstractRouteDef]) -> List[AbstractRoute]:
        return self.router.add_routes(routes)

    @property
    def on_response_prepare(self) -> _RespPrepareSignal:
        return self._on_response_prepare

    @property
    def on_startup(self) -> _AppSignal:
        return self._on_startup

    @property
    def on_shutdown(self) -> _AppSignal:
        return self._on_shutdown

    @property
    def on_cleanup(self) -> _AppSignal:
        return self._on_cleanup

    @property
    def cleanup_ctx(self) -> "CleanupContext":
        return self._cleanup_ctx

    @property
    def router(self) -> UrlDispatcher:
        return self._router

    @property
    def middlewares(self) -> _Middlewares:
        return self._middlewares

    def _make_handler(
        self,
        *,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        access_log_class: Type[AbstractAccessLogger] = AccessLogger,
        **kwargs: Any,
    ) -> Server:

        if not issubclass(access_log_class, AbstractAccessLogger):
            raise TypeError(
                "access_log_class must be subclass of "
                "aiohttp.abc.AbstractAccessLogger, got {}".format(access_log_class)
            )

        self._set_loop(loop)
        self.freeze()

        kwargs["debug"] = self._debug
        kwargs["access_log_class"] = access_log_class
        if self._handler_args:
            for k, v in self._handler_args.items():
                kwargs[k] = v

        return Server(
            self._handle,  
            request_factory=self._make_request,
            loop=self._loop,
            **kwargs,
        )

    def make_handler(
        self,
        *,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        access_log_class: Type[AbstractAccessLogger] = AccessLogger,
        **kwargs: Any,
    ) -> Server:

        warnings.warn(
            "Application.make_handler(...) is deprecated, " "use AppRunner API instead",
            DeprecationWarning,
            stacklevel=2,
        )

        return self._make_handler(
            loop=loop, access_log_class=access_log_class, **kwargs
        )

    async def startup(self) -> None:
        """Causes on_startup signal

        Should be called in the event loop along with the request handler.
        """
        await self.on_startup.send(self)

    async def shutdown(self) -> None:
        """Causes on_shutdown signal

        Should be called before cleanup()
        """
        await self.on_shutdown.send(self)

    async def cleanup(self) -> None:
        """Causes on_cleanup signal

        Should be called after shutdown()
        """
        if self.on_cleanup.frozen:
            await self.on_cleanup.send(self)
        else:
            
            await self._cleanup_ctx._on_cleanup(self)

    def _make_request(
        self,
        message: RawRequestMessage,
        payload: StreamReader,
        protocol: RequestHandler,
        writer: AbstractStreamWriter,
        task: "asyncio.Task[None]",
        _cls: Type[Request] = Request,
    ) -> Request:
        return _cls(
            message,
            payload,
            protocol,
            writer,
            task,
            self._loop,
            client_max_size=self._client_max_size,
        )

    def _prepare_middleware(self) -> Iterator[Tuple[_Middleware, bool]]:
        for m in reversed(self._middlewares):
            if getattr(m, "__middleware_version__", None) == 1:
                yield m, True
            else:
                warnings.warn(
                    'old-style middleware "{!r}" deprecated, ' "see ".format(m),
                    DeprecationWarning,
                    stacklevel=2,
                )
                yield m, False

        yield _fix_request_current_app(self), True

    async def _handle(self, request: Request) -> StreamResponse:
        loop = asyncio.get_event_loop()
        debug = loop.get_debug()
        match_info = await self._router.resolve(request)
        if debug:  
            if not isinstance(match_info, AbstractMatchInfo):
                raise TypeError(
                    "match_info should be AbstractMatchInfo "
                    "instance, not {!r}".format(match_info)
                )
        match_info.add_app(self)

        match_info.freeze()

        resp = None
        request._match_info = match_info
        expect = request.headers.get(hdrs.EXPECT)
        if expect:
            resp = await match_info.expect_handler(request)
            await request.writer.drain()

        if resp is None:
            handler = match_info.handler

            if self._run_middlewares:
                for app in match_info.apps[::-1]:
                    for m, new_style in app._middlewares_handlers:  
                        if new_style:
                            handler = update_wrapper(
                                partial(m, handler=handler), handler
                            )
                        else:
                            handler = await m(app, handler)  

            resp = await handler(request)

        return resp

    def __call__(self) -> "Application":
        """gunicorn compatibility"""
        return self

    def __repr__(self) -> str:
        return "<Application 0x{:x}>".format(id(self))

    def __bool__(self) -> bool:
        return True


class CleanupError(RuntimeError):
    @property
    def exceptions(self) -> List[BaseException]:
        return cast(List[BaseException], self.args[1])


if TYPE_CHECKING:  
    _CleanupContextBase = FrozenList[Callable[[Application], AsyncIterator[None]]]
else:
    _CleanupContextBase = FrozenList


class CleanupContext(_CleanupContextBase):
    def __init__(self) -> None:
        super().__init__()
        self._exits = []  

    async def _on_startup(self, app: Application) -> None:
        for cb in self:
            it = cb(app).__aiter__()
            await it.__anext__()
            self._exits.append(it)

    async def _on_cleanup(self, app: Application) -> None:
        errors = []
        for it in reversed(self._exits):
            try:
                await it.__anext__()
            except StopAsyncIteration:
                pass
            except Exception as exc:
                errors.append(exc)
            else:
                errors.append(RuntimeError(f"{it!r} has more than one 'yield'"))
        if errors:
            if len(errors) == 1:
                raise errors[0]
            else:
                raise CleanupError("Multiple errors on cleanup stage", errors)
