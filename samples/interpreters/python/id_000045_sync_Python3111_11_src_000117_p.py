from .interfaces import *
from .winstructs import *


ObjectFromLresultPrototype = WINFUNCTYPE(HRESULT, LRESULT, REFIID, WPARAM, POINTER(PVOID))
ObjectFromLresultParams = ((1, 'lResult'), (1, 'riid'), (1, 'wParam'), (1, 'ppvObject'))



NtAlpcCreatePortPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, POBJECT_ATTRIBUTES, PALPC_PORT_ATTRIBUTES)
NtAlpcCreatePortParams = ((1, 'PortHandle'), (1, 'ObjectAttributes'), (1, 'PortAttributes'))



NtAlpcQueryInformationPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, ALPC_PORT_INFORMATION_CLASS, PVOID, ULONG, PULONG)
NtAlpcQueryInformationParams = ((1, 'PortHandle'), (1, 'PortInformationClass'), (1, 'PortInformation'), (1, 'Length'), (1, 'ReturnLength'))



NtAlpcQueryInformationMessagePrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PPORT_MESSAGE, ALPC_MESSAGE_INFORMATION_CLASS, PVOID, ULONG, PULONG)
NtAlpcQueryInformationMessageParams = ((1, 'PortHandle'), (1, 'PortMessage'), (1, 'MessageInformationClass'), (1, 'MessageInformation'), (1, 'Length'), (1, 'ReturnLength'))



NtConnectPortPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, PUNICODE_STRING, PSECURITY_QUALITY_OF_SERVICE, PPORT_VIEW, PREMOTE_PORT_VIEW, PULONG, PVOID, PULONG)
NtConnectPortParams = ((1, 'PortHandle'), (1, 'PortName'), (1, 'SecurityQos'), (1, 'ClientView'), (1, 'ServerView'), (1, 'MaxMessageLength'), (1, 'ConnectionInformation'), (1, 'ConnectionInformationLength'))



NtAlpcConnectPortPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, PUNICODE_STRING, POBJECT_ATTRIBUTES, PALPC_PORT_ATTRIBUTES, ULONG, PSID, PPORT_MESSAGE, PULONG, PALPC_MESSAGE_ATTRIBUTES, PALPC_MESSAGE_ATTRIBUTES, PLARGE_INTEGER)
NtAlpcConnectPortParams = ((1, 'PortHandle'), (1, 'PortName'), (1, 'ObjectAttributes'), (1, 'PortAttributes'), (1, 'Flags'), (1, 'RequiredServerSid'), (1, 'ConnectionMessage'), (1, 'BufferLength'), (1, 'OutMessageAttributes'), (1, 'InMessageAttributes'), (1, 'Timeout'))



NtAlpcConnectPortExPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, POBJECT_ATTRIBUTES, POBJECT_ATTRIBUTES, PALPC_PORT_ATTRIBUTES, ULONG, PSECURITY_DESCRIPTOR, PPORT_MESSAGE, PSIZE_T, PALPC_MESSAGE_ATTRIBUTES, PALPC_MESSAGE_ATTRIBUTES, PLARGE_INTEGER)
NtAlpcConnectPortExParams = ((1, 'PortHandle'), (1, 'ConnectionPortObjectAttributes'), (1, 'ClientPortObjectAttributes'), (1, 'PortAttributes'), (1, 'Flags'), (1, 'ServerSecurityRequirements'), (1, 'ConnectionMessage'), (1, 'BufferLength'), (1, 'OutMessageAttributes'), (1, 'InMessageAttributes'), (1, 'Timeout'))



NtAlpcAcceptConnectPortPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, HANDLE, ULONG, POBJECT_ATTRIBUTES, PALPC_PORT_ATTRIBUTES, PVOID, PPORT_MESSAGE, PALPC_MESSAGE_ATTRIBUTES, BOOLEAN)
NtAlpcAcceptConnectPortParams = ((1, 'PortHandle'), (1, 'ConnectionPortHandle'), (1, 'Flags'), (1, 'ObjectAttributes'), (1, 'PortAttributes'), (1, 'PortContext'), (1, 'ConnectionRequest'), (1, 'ConnectionMessageAttributes'), (1, 'AcceptConnection'))



AlpcInitializeMessageAttributePrototype = WINFUNCTYPE(NTSTATUS, ULONG, PALPC_MESSAGE_ATTRIBUTES, ULONG, PULONG)
AlpcInitializeMessageAttributeParams = ((1, 'AttributeFlags'), (1, 'Buffer'), (1, 'BufferSize'), (1, 'RequiredBufferSize'))



AlpcGetMessageAttributePrototype = WINFUNCTYPE(PVOID, PALPC_MESSAGE_ATTRIBUTES, ULONG)
AlpcGetMessageAttributeParams = ((1, 'Buffer'), (1, 'AttributeFlag'))



NtAlpcSendWaitReceivePortPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, ULONG, PPORT_MESSAGE, PALPC_MESSAGE_ATTRIBUTES, PPORT_MESSAGE, PSIZE_T, PALPC_MESSAGE_ATTRIBUTES, PLARGE_INTEGER)
NtAlpcSendWaitReceivePortParams = ((1, 'PortHandle'), (1, 'Flags'), (1, 'SendMessage'), (1, 'SendMessageAttributes'), (1, 'ReceiveMessage'), (1, 'BufferLength'), (1, 'ReceiveMessageAttributes'), (1, 'Timeout'))



NtAlpcDisconnectPortPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, ULONG)
NtAlpcDisconnectPortParams = ((1, 'PortHandle'), (1, 'Flags'))



NtAlpcCreatePortSectionPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, ULONG, HANDLE, SIZE_T, PALPC_HANDLE, PSIZE_T)
NtAlpcCreatePortSectionParams = ((1, 'PortHandle'), (1, 'Flags'), (1, 'SectionHandle'), (1, 'SectionSize'), (1, 'AlpcSectionHandle'), (1, 'ActualSectionSize'))



NtAlpcDeletePortSectionPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, ULONG, ALPC_HANDLE)
NtAlpcDeletePortSectionParams = ((1, 'PortHandle'), (1, 'Flags'), (1, 'SectionHandle'))



NtAlpcCreateResourceReservePrototype = WINFUNCTYPE(NTSTATUS, HANDLE, ULONG, SIZE_T, PALPC_HANDLE)
NtAlpcCreateResourceReserveParams = ((1, 'PortHandle'), (1, 'Flags'), (1, 'MessageSize'), (1, 'ResourceId'))



NtAlpcDeleteResourceReservePrototype = WINFUNCTYPE(NTSTATUS, HANDLE, ULONG, ALPC_HANDLE)
NtAlpcDeleteResourceReserveParams = ((1, 'PortHandle'), (1, 'Flags'), (1, 'ResourceId'))



NtAlpcCreateSectionViewPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, ULONG, PALPC_DATA_VIEW_ATTR)
NtAlpcCreateSectionViewParams = ((1, 'PortHandle'), (1, 'Flags'), (1, 'ViewAttributes'))



NtAlpcDeleteSectionViewPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, ULONG, PVOID)
NtAlpcDeleteSectionViewParams = ((1, 'PortHandle'), (1, 'Flags'), (1, 'ViewBase'))



NtAlpcCreateSecurityContextPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, ULONG, PALPC_SECURITY_ATTR)
NtAlpcCreateSecurityContextParams = ((1, 'PortHandle'), (1, 'Flags'), (1, 'SecurityAttribute'))



NtAlpcDeleteSecurityContextPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, ULONG, ALPC_HANDLE)
NtAlpcDeleteSecurityContextParams = ((1, 'PortHandle'), (1, 'Flags'), (1, 'ContextHandle'))



NtAlpcRevokeSecurityContextPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, ULONG, ALPC_HANDLE)
NtAlpcRevokeSecurityContextParams = ((1, 'PortHandle'), (1, 'Flags'), (1, 'ContextHandle'))



NtAlpcImpersonateClientOfPortPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PPORT_MESSAGE, PVOID)
NtAlpcImpersonateClientOfPortParams = ((1, 'PortHandle'), (1, 'Message'), (1, 'Flags'))



TpCallbackSendAlpcMessageOnCompletionPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, HANDLE, ULONG, PPORT_MESSAGE)
TpCallbackSendAlpcMessageOnCompletionParams = ((1, 'TpHandle'), (1, 'PortHandle'), (1, 'Flags'), (1, 'SendMessage'))



AddAtomAPrototype = WINFUNCTYPE(ATOM, LPCSTR)
AddAtomAParams = ((1, 'lpString'),)



AddAtomWPrototype = WINFUNCTYPE(ATOM, LPCWSTR)
AddAtomWParams = ((1, 'lpString'),)



GlobalAddAtomAPrototype = WINFUNCTYPE(ATOM, LPCSTR)
GlobalAddAtomAParams = ((1, 'lpString'),)



GlobalAddAtomExAPrototype = WINFUNCTYPE(ATOM, LPCSTR, DWORD)
GlobalAddAtomExAParams = ((1, 'lpString'), (1, 'Flags'))



GlobalAddAtomExWPrototype = WINFUNCTYPE(ATOM, LPCWSTR, DWORD)
GlobalAddAtomExWParams = ((1, 'lpString'), (1, 'Flags'))



GlobalAddAtomWPrototype = WINFUNCTYPE(ATOM, LPCWSTR)
GlobalAddAtomWParams = ((1, 'lpString'),)



GlobalDeleteAtomPrototype = WINFUNCTYPE(ATOM, ATOM)
GlobalDeleteAtomParams = ((1, 'nAtom'),)



GlobalGetAtomNameAPrototype = WINFUNCTYPE(UINT, ATOM, LPSTR, INT)
GlobalGetAtomNameAParams = ((1, 'nAtom'), (1, 'lpBuffer'), (1, 'nSize'))



GlobalGetAtomNameWPrototype = WINFUNCTYPE(UINT, ATOM, LPWSTR, INT)
GlobalGetAtomNameWParams = ((1, 'nAtom'), (1, 'lpBuffer'), (1, 'nSize'))



CM_Enumerate_ClassesPrototype = WINFUNCTYPE(CONFIGRET, ULONG, LPGUID, ULONG)
CM_Enumerate_ClassesParams = ((1, 'ulClassIndex'), (1, 'ClassGuid'), (1, 'ulFlags'))



CM_Enumerate_Classes_ExPrototype = WINFUNCTYPE(CONFIGRET, ULONG, LPGUID, ULONG, HMACHINE)
CM_Enumerate_Classes_ExParams = ((1, 'ulClassIndex'), (1, 'ClassGuid'), (1, 'ulFlags'), (1, 'hMachine'))



CM_Get_First_Log_ConfPrototype = WINFUNCTYPE(CONFIGRET, PLOG_CONF, DEVINST, ULONG)
CM_Get_First_Log_ConfParams = ((1, 'plcLogConf'), (1, 'dnDevInst'), (1, 'ulFlags'))



CM_Get_First_Log_Conf_ExPrototype = WINFUNCTYPE(CONFIGRET, PLOG_CONF, DEVINST, ULONG, HMACHINE)
CM_Get_First_Log_Conf_ExParams = ((1, 'plcLogConf'), (1, 'dnDevInst'), (1, 'ulFlags'), (1, 'hMachine'))



CM_Get_Log_Conf_PriorityPrototype = WINFUNCTYPE(CONFIGRET, LOG_CONF, PPRIORITY, ULONG)
CM_Get_Log_Conf_PriorityParams = ((1, 'lcLogConf'), (1, 'pPriority'), (1, 'ulFlags'))



CM_Get_Log_Conf_Priority_ExPrototype = WINFUNCTYPE(CONFIGRET, LOG_CONF, PPRIORITY, ULONG, HMACHINE)
CM_Get_Log_Conf_Priority_ExParams = ((1, 'lcLogConf'), (1, 'pPriority'), (1, 'ulFlags'), (1, 'hMachine'))



CM_Get_Next_Log_ConfPrototype = WINFUNCTYPE(CONFIGRET, PLOG_CONF, LOG_CONF, ULONG)
CM_Get_Next_Log_ConfParams = ((1, 'plcLogConf'), (1, 'lcLogConf'), (1, 'ulFlags'))



CM_Get_Next_Log_Conf_ExPrototype = WINFUNCTYPE(CONFIGRET, PLOG_CONF, LOG_CONF, ULONG, HMACHINE)
CM_Get_Next_Log_Conf_ExParams = ((1, 'plcLogConf'), (1, 'lcLogConf'), (1, 'ulFlags'), (1, 'hMachine'))



CM_Free_Res_Des_HandlePrototype = WINFUNCTYPE(CONFIGRET, RES_DES)
CM_Free_Res_Des_HandleParams = ((1, 'rdResDes'),)



CM_Get_ChildPrototype = WINFUNCTYPE(CONFIGRET, PDEVINST, DEVINST, ULONG)
CM_Get_ChildParams = ((1, 'pdnDevInst'), (1, 'dnDevInst'), (1, 'ulFlags'))



CM_Get_Child_ExPrototype = WINFUNCTYPE(CONFIGRET, PDEVINST, DEVINST, ULONG, HMACHINE)
CM_Get_Child_ExParams = ((1, 'pdnDevInst'), (1, 'dnDevInst'), (1, 'ulFlags'), (1, 'hMachine'))



CM_Get_Next_Res_DesPrototype = WINFUNCTYPE(CONFIGRET, PRES_DES, RES_DES, RESOURCEID, PRESOURCEID, ULONG)
CM_Get_Next_Res_DesParams = ((1, 'prdResDes'), (1, 'rdResDes'), (1, 'ForResource'), (1, 'pResourceID'), (1, 'ulFlags'))



CM_Get_ParentPrototype = WINFUNCTYPE(CONFIGRET, PDEVINST, DEVINST, ULONG)
CM_Get_ParentParams = ((1, 'pdnDevInst'), (1, 'dnDevInst'), (1, 'ulFlags'))



CM_Get_Parent_ExPrototype = WINFUNCTYPE(CONFIGRET, PDEVINST, DEVINST, ULONG, HMACHINE)
CM_Get_Parent_ExParams = ((1, 'pdnDevInst'), (1, 'dnDevInst'), (1, 'ulFlags'), (1, 'hMachine'))



CM_Get_Res_Des_DataPrototype = WINFUNCTYPE(CONFIGRET, RES_DES, PVOID, ULONG, ULONG)
CM_Get_Res_Des_DataParams = ((1, 'rdResDes'), (1, 'Buffer'), (1, 'BufferLen'), (1, 'ulFlags'))



CM_Get_Next_Res_Des_ExPrototype = WINFUNCTYPE(CONFIGRET, PRES_DES, RES_DES, RESOURCEID, PRESOURCEID, ULONG, HMACHINE)
CM_Get_Next_Res_Des_ExParams = ((1, 'prdResDes'), (1, 'rdResDes'), (1, 'ForResource'), (1, 'pResourceID'), (1, 'ulFlags'), (1, 'hMachine'))



CM_Get_Res_Des_Data_SizePrototype = WINFUNCTYPE(CONFIGRET, PULONG, RES_DES, ULONG)
CM_Get_Res_Des_Data_SizeParams = ((1, 'pulSize'), (1, 'rdResDes'), (1, 'ulFlags'))



CM_Get_Res_Des_Data_Size_ExPrototype = WINFUNCTYPE(CONFIGRET, PULONG, RES_DES, ULONG, HMACHINE)
CM_Get_Res_Des_Data_Size_ExParams = ((1, 'pulSize'), (1, 'rdResDes'), (1, 'ulFlags'), (1, 'hMachine'))



CM_Get_SiblingPrototype = WINFUNCTYPE(CONFIGRET, PDEVINST, DEVINST, ULONG)
CM_Get_SiblingParams = ((1, 'pdnDevInst'), (1, 'dnDevInst'), (1, 'ulFlags'))



CM_Get_Sibling_ExPrototype = WINFUNCTYPE(CONFIGRET, PDEVINST, DEVINST, ULONG, HMACHINE)
CM_Get_Sibling_ExParams = ((1, 'pdnDevInst'), (1, 'dnDevInst'), (1, 'ulFlags'), (1, 'hMachine'))



CM_Get_VersionPrototype = WINFUNCTYPE(WORD)
CM_Get_VersionParams = ()



CM_Get_Version_ExPrototype = WINFUNCTYPE(WORD, HMACHINE)
CM_Get_Version_ExParams = ((1, 'hMachine'),)



CM_Locate_DevNodeAPrototype = WINFUNCTYPE(CONFIGRET, PDEVINST, DEVINSTID_A, ULONG)
CM_Locate_DevNodeAParams = ((1, 'pdnDevInst'), (1, 'pDeviceID'), (1, 'ulFlags'))



CM_Locate_DevNodeWPrototype = WINFUNCTYPE(CONFIGRET, PDEVINST, DEVINSTID_W, ULONG)
CM_Locate_DevNodeWParams = ((1, 'pdnDevInst'), (1, 'pDeviceID'), (1, 'ulFlags'))



CM_Locate_DevNode_ExAPrototype = WINFUNCTYPE(CONFIGRET, PDEVINST, DEVINSTID_A, ULONG, HMACHINE)
CM_Locate_DevNode_ExAParams = ((1, 'pdnDevInst'), (1, 'pDeviceID'), (1, 'ulFlags'), (1, 'hMachine'))



CM_Locate_DevNode_ExWPrototype = WINFUNCTYPE(CONFIGRET, PDEVINST, DEVINSTID_W, ULONG, HMACHINE)
CM_Locate_DevNode_ExWParams = ((1, 'pdnDevInst'), (1, 'pDeviceID'), (1, 'ulFlags'), (1, 'hMachine'))



CoInitializeExPrototype = WINFUNCTYPE(HRESULT, LPVOID, DWORD)
CoInitializeExParams = ((1, 'pvReserved'), (1, 'dwCoInit'))



CoInitializeSecurityPrototype = WINFUNCTYPE(HRESULT, PSECURITY_DESCRIPTOR, LONG, POINTER(SOLE_AUTHENTICATION_SERVICE), PVOID, DWORD, DWORD, PVOID, DWORD, PVOID)
CoInitializeSecurityParams = ((1, 'pSecDesc'), (1, 'cAuthSvc'), (1, 'asAuthSvc'), (1, 'pReserved1'), (1, 'dwAuthnLevel'), (1, 'dwImpLevel'), (1, 'pAuthList'), (1, 'dwCapabilities'), (1, 'pReserved3'))



CoCreateInstancePrototype = WINFUNCTYPE(HRESULT, REFCLSID, LPUNKNOWN, DWORD, REFIID, POINTER(LPVOID))
CoCreateInstanceParams = ((1, 'rclsid'), (1, 'pUnkOuter'), (1, 'dwClsContext'), (1, 'riid'), (1, 'ppv'))



CoCreateInstanceExPrototype = WINFUNCTYPE(HRESULT, REFCLSID, POINTER(IUnknown), DWORD, POINTER(COSERVERINFO), DWORD, POINTER(MULTI_QI))
CoCreateInstanceExParams = ((1, 'rclsid'), (1, 'punkOuter'), (1, 'dwClsCtx'), (1, 'pServerInfo'), (1, 'dwCount'), (1, 'pResults'))



CoGetClassObjectPrototype = WINFUNCTYPE(HRESULT, REFCLSID, DWORD, LPVOID, REFIID, POINTER(LPVOID))
CoGetClassObjectParams = ((1, 'rclsid'), (1, 'dwClsContext'), (1, 'pvReserved'), (1, 'riid'), (1, 'ppv'))



CoGetInterceptorPrototype = WINFUNCTYPE(HRESULT, REFIID, POINTER(IUnknown), REFIID, POINTER(PVOID))
CoGetInterceptorParams = ((1, 'iidIntercepted'), (1, 'punkOuter'), (1, 'iid'), (1, 'ppv'))



CLSIDFromProgIDPrototype = WINFUNCTYPE(HRESULT, LPCOLESTR, LPCLSID)
CLSIDFromProgIDParams = ((1, 'lpszProgID'), (1, 'lpclsid'))



CoTaskMemFreePrototype = WINFUNCTYPE(PVOID, LPVOID)
CoTaskMemFreeParams = ((1, 'pv'),)



SafeArrayCreatePrototype = WINFUNCTYPE(LPSAFEARRAY, VARTYPE, UINT, POINTER(SAFEARRAYBOUND))
SafeArrayCreateParams = ((1, 'vt'), (1, 'cDims'), (1, 'rgsabound'))



SafeArrayCreateVectorPrototype = WINFUNCTYPE(LPSAFEARRAY, VARTYPE, LONG, ULONG)
SafeArrayCreateVectorParams = ((1, 'vt'), (1, 'lLbound'), (1, 'cElements'))



SafeArrayDestroyPrototype = WINFUNCTYPE(HRESULT, POINTER(SAFEARRAY))
SafeArrayDestroyParams = ((1, 'psa'),)



SafeArrayDestroyDataPrototype = WINFUNCTYPE(HRESULT, POINTER(SAFEARRAY))
SafeArrayDestroyDataParams = ((1, 'psa'),)



SafeArrayGetElementPrototype = WINFUNCTYPE(HRESULT, POINTER(SAFEARRAY), POINTER(LONG), PVOID)
SafeArrayGetElementParams = ((1, 'psa'), (1, 'rgIndices'), (1, 'pv'))



SafeArrayGetElemsizePrototype = WINFUNCTYPE(UINT, POINTER(SAFEARRAY))
SafeArrayGetElemsizeParams = ((1, 'psa'),)



SafeArrayGetLBoundPrototype = WINFUNCTYPE(HRESULT, POINTER(SAFEARRAY), UINT, POINTER(LONG))
SafeArrayGetLBoundParams = ((1, 'psa'), (1, 'nDim'), (1, 'plLbound'))



SafeArrayGetUBoundPrototype = WINFUNCTYPE(HRESULT, POINTER(SAFEARRAY), UINT, POINTER(LONG))
SafeArrayGetUBoundParams = ((1, 'psa'), (1, 'nDim'), (1, 'plUbound'))



SafeArrayGetDimPrototype = WINFUNCTYPE(UINT, POINTER(SAFEARRAY))
SafeArrayGetDimParams = ((1, 'psa'),)



SafeArrayPutElementPrototype = WINFUNCTYPE(HRESULT, POINTER(SAFEARRAY), POINTER(LONG), PVOID)
SafeArrayPutElementParams = ((1, 'psa'), (1, 'rgIndices'), (1, 'pv'))



SafeArrayGetVartypePrototype = WINFUNCTYPE(HRESULT, POINTER(SAFEARRAY), POINTER(VARTYPE))
SafeArrayGetVartypeParams = ((1, 'psa'), (1, 'pvt'))



SysFreeStringPrototype = WINFUNCTYPE(VOID, BSTR)
SysFreeStringParams = ((1, 'bstrString'),)



SafeArrayCopyPrototype = WINFUNCTYPE(HRESULT, POINTER(SAFEARRAY), POINTER(LPSAFEARRAY))
SafeArrayCopyParams = ((1, 'psa'), (1, 'ppsaOut'))



SafeArrayCopyDataPrototype = WINFUNCTYPE(HRESULT, POINTER(SAFEARRAY), POINTER(SAFEARRAY))
SafeArrayCopyDataParams = ((1, 'psaSource'), (1, 'psaTarget'))



SysAllocStringPrototype = WINFUNCTYPE(PVOID, POINTER(OLECHAR))
SysAllocStringParams = ((1, 'psz'),)



SysFreeStringPrototype = WINFUNCTYPE(VOID, BSTR)
SysFreeStringParams = ((1, 'bstrString'),)



CryptCATAdminCalcHashFromFileHandlePrototype = WINFUNCTYPE(BOOL, HANDLE, POINTER(DWORD), POINTER(BYTE), DWORD)
CryptCATAdminCalcHashFromFileHandleParams = ((1, 'hFile'), (1, 'pcbHash'), (1, 'pbHash'), (1, 'dwFlags'))



CryptCATAdminCalcHashFromFileHandle2Prototype = WINFUNCTYPE(BOOL, HCATADMIN, HANDLE, POINTER(DWORD), POINTER(BYTE), DWORD)
CryptCATAdminCalcHashFromFileHandle2Params = ((1, 'hCatAdmin'), (1, 'hFile'), (1, 'pcbHash'), (1, 'pbHash'), (1, 'dwFlags'))



CryptCATAdminEnumCatalogFromHashPrototype = WINFUNCTYPE(HCATINFO, HCATADMIN, POINTER(BYTE), DWORD, DWORD, POINTER(HCATINFO))
CryptCATAdminEnumCatalogFromHashParams = ((1, 'hCatAdmin'), (1, 'pbHash'), (1, 'cbHash'), (1, 'dwFlags'), (1, 'phPrevCatInfo'))



CryptCATAdminAcquireContextPrototype = WINFUNCTYPE(BOOL, POINTER(HCATADMIN), POINTER(GUID), DWORD)
CryptCATAdminAcquireContextParams = ((1, 'phCatAdmin'), (1, 'pgSubsystem'), (1, 'dwFlags'))



CryptCATAdminAcquireContext2Prototype = WINFUNCTYPE(BOOL, POINTER(HCATADMIN), POINTER(GUID), PCWSTR, PCCERT_STRONG_SIGN_PARA, DWORD)
CryptCATAdminAcquireContext2Params = ((1, 'phCatAdmin'), (1, 'pgSubsystem'), (1, 'pwszHashAlgorithm'), (1, 'pStrongHashPolicy'), (1, 'dwFlags'))



CryptCATCatalogInfoFromContextPrototype = WINFUNCTYPE(BOOL, HCATINFO, POINTER(CATALOG_INFO), DWORD)
CryptCATCatalogInfoFromContextParams = ((1, 'hCatInfo'), (1, 'psCatInfo'), (1, 'dwFlags'))



CryptCATAdminReleaseCatalogContextPrototype = WINFUNCTYPE(BOOL, HCATADMIN, HCATINFO, DWORD)
CryptCATAdminReleaseCatalogContextParams = ((1, 'hCatAdmin'), (1, 'hCatInfo'), (1, 'dwFlags'))



CryptCATAdminReleaseContextPrototype = WINFUNCTYPE(BOOL, HCATADMIN, DWORD)
CryptCATAdminReleaseContextParams = ((1, 'hCatAdmin'), (1, 'dwFlags'))



CryptCATGetAttrInfoPrototype = WINFUNCTYPE(POINTER(CRYPTCATATTRIBUTE), HANDLE, POINTER(CRYPTCATMEMBER), LPWSTR)
CryptCATGetAttrInfoParams = ((1, 'hCatalog'), (1, 'pCatMember'), (1, 'pwszReferenceTag'))



CryptCATGetMemberInfoPrototype = WINFUNCTYPE(POINTER(CRYPTCATMEMBER), HANDLE, LPWSTR)
CryptCATGetMemberInfoParams = ((1, 'hCatalog'), (1, 'pwszReferenceTag'))



CryptCATGetAttrInfoPrototype = WINFUNCTYPE(POINTER(CRYPTCATATTRIBUTE), HANDLE, POINTER(CRYPTCATMEMBER), LPWSTR)
CryptCATGetAttrInfoParams = ((1, 'hCatalog'), (1, 'pCatMember'), (1, 'pwszReferenceTag'))



CryptCATEnumerateCatAttrPrototype = WINFUNCTYPE(POINTER(CRYPTCATATTRIBUTE), HANDLE, POINTER(CRYPTCATATTRIBUTE))
CryptCATEnumerateCatAttrParams = ((1, 'hCatalog'), (1, 'pPrevAttr'))



CryptCATEnumerateAttrPrototype = WINFUNCTYPE(POINTER(CRYPTCATATTRIBUTE), HANDLE, POINTER(CRYPTCATMEMBER), POINTER(CRYPTCATATTRIBUTE))
CryptCATEnumerateAttrParams = ((1, 'hCatalog'), (1, 'pCatMember'), (1, 'pPrevAttr'))



CryptCATEnumerateMemberPrototype = WINFUNCTYPE(POINTER(CRYPTCATMEMBER), HANDLE, POINTER(CRYPTCATMEMBER))
CryptCATEnumerateMemberParams = ((1, 'hCatalog'), (1, 'pPrevMember'))



CryptQueryObjectPrototype = WINFUNCTYPE(BOOL, DWORD, PVOID, DWORD, DWORD, DWORD, POINTER(DWORD), POINTER(DWORD), POINTER(DWORD), POINTER(HCERTSTORE), POINTER(HCRYPTMSG), POINTER(PVOID))
CryptQueryObjectParams = ((1, 'dwObjectType'), (1, 'pvObject'), (1, 'dwExpectedContentTypeFlags'), (1, 'dwExpectedFormatTypeFlags'), (1, 'dwFlags'), (1, 'pdwMsgAndCertEncodingType'), (1, 'pdwContentType'), (1, 'pdwFormatType'), (1, 'phCertStore'), (1, 'phMsg'), (1, 'ppvContext'))



CryptMsgGetParamPrototype = WINFUNCTYPE(BOOL, HCRYPTMSG, DWORD, DWORD, PVOID, POINTER(DWORD))
CryptMsgGetParamParams = ((1, 'hCryptMsg'), (1, 'dwParamType'), (1, 'dwIndex'), (1, 'pvData'), (1, 'pcbData'))



CryptDecodeObjectPrototype = WINFUNCTYPE(BOOL, DWORD, LPCSTR, POINTER(BYTE), DWORD, DWORD, PVOID, POINTER(DWORD))
CryptDecodeObjectParams = ((1, 'dwCertEncodingType'), (1, 'lpszStructType'), (1, 'pbEncoded'), (1, 'cbEncoded'), (1, 'dwFlags'), (1, 'pvStructInfo'), (1, 'pcbStructInfo'))



CertFindCertificateInStorePrototype = WINFUNCTYPE(PCCERT_CONTEXT, HCERTSTORE, DWORD, DWORD, DWORD, PVOID, PCCERT_CONTEXT)
CertFindCertificateInStoreParams = ((1, 'hCertStore'), (1, 'dwCertEncodingType'), (1, 'dwFindFlags'), (1, 'dwFindType'), (1, 'pvFindPara'), (1, 'pPrevCertContext'))



CertGetNameStringAPrototype = WINFUNCTYPE(DWORD, PCCERT_CONTEXT, DWORD, DWORD, PVOID, LPCSTR, DWORD)
CertGetNameStringAParams = ((1, 'pCertContext'), (1, 'dwType'), (1, 'dwFlags'), (1, 'pvTypePara'), (1, 'pszNameString'), (1, 'cchNameString'))



CertGetNameStringWPrototype = WINFUNCTYPE(DWORD, PCCERT_CONTEXT, DWORD, DWORD, PVOID, LPWSTR, DWORD)
CertGetNameStringWParams = ((1, 'pCertContext'), (1, 'dwType'), (1, 'dwFlags'), (1, 'pvTypePara'), (1, 'pszNameString'), (1, 'cchNameString'))



CertGetCertificateChainPrototype = WINFUNCTYPE(BOOL, HCERTCHAINENGINE, PCCERT_CONTEXT, LPFILETIME, HCERTSTORE, PCERT_CHAIN_PARA, DWORD, LPVOID, POINTER(PCCERT_CHAIN_CONTEXT))
CertGetCertificateChainParams = ((1, 'hChainEngine'), (1, 'pCertContext'), (1, 'pTime'), (1, 'hAdditionalStore'), (1, 'pChainPara'), (1, 'dwFlags'), (1, 'pvReserved'), (1, 'ppChainContext'))



CertCreateSelfSignCertificatePrototype = WINFUNCTYPE(PCCERT_CONTEXT, HCRYPTPROV_OR_NCRYPT_KEY_HANDLE, PCERT_NAME_BLOB, DWORD, PCRYPT_KEY_PROV_INFO, PCRYPT_ALGORITHM_IDENTIFIER, PSYSTEMTIME, PSYSTEMTIME, PCERT_EXTENSIONS)
CertCreateSelfSignCertificateParams = ((1, 'hCryptProvOrNCryptKey'), (1, 'pSubjectIssuerBlob'), (1, 'dwFlags'), (1, 'pKeyProvInfo'), (1, 'pSignatureAlgorithm'), (1, 'pStartTime'), (1, 'pEndTime'), (1, 'pExtensions'))



CertStrToNameAPrototype = WINFUNCTYPE(BOOL, DWORD, LPCSTR, DWORD, PVOID, POINTER(BYTE), POINTER(DWORD), POINTER(LPCSTR))
CertStrToNameAParams = ((1, 'dwCertEncodingType'), (1, 'pszX500'), (1, 'dwStrType'), (1, 'pvReserved'), (1, 'pbEncoded'), (1, 'pcbEncoded'), (1, 'ppszError'))



CertStrToNameWPrototype = WINFUNCTYPE(BOOL, DWORD, LPWSTR, DWORD, PVOID, POINTER(BYTE), POINTER(DWORD), POINTER(LPWSTR))
CertStrToNameWParams = ((1, 'dwCertEncodingType'), (1, 'pszX500'), (1, 'dwStrType'), (1, 'pvReserved'), (1, 'pbEncoded'), (1, 'pcbEncoded'), (1, 'ppszError'))



CertOpenStorePrototype = WINFUNCTYPE(HCERTSTORE, LPCSTR, DWORD, HCRYPTPROV_LEGACY, DWORD, PVOID)
CertOpenStoreParams = ((1, 'lpszStoreProvider'), (1, 'dwMsgAndCertEncodingType'), (1, 'hCryptProv'), (1, 'dwFlags'), (1, 'pvPara'))



CertAddCertificateContextToStorePrototype = WINFUNCTYPE(BOOL, HCERTSTORE, PCCERT_CONTEXT, DWORD, POINTER(PCCERT_CONTEXT))
CertAddCertificateContextToStoreParams = ((1, 'hCertStore'), (1, 'pCertContext'), (1, 'dwAddDisposition'), (1, 'ppStoreContext'))



CertFreeCertificateContextPrototype = WINFUNCTYPE(BOOL, PCCERT_CONTEXT)
CertFreeCertificateContextParams = ((1, 'pCertContext'),)



PFXExportCertStoreExPrototype = WINFUNCTYPE(BOOL, HCERTSTORE, POINTER(CRYPT_DATA_BLOB), LPCWSTR, PVOID, DWORD)
PFXExportCertStoreExParams = ((1, 'hStore'), (1, 'pPFX'), (1, 'szPassword'), (1, 'pvPara'), (1, 'dwFlags'))



PFXImportCertStorePrototype = WINFUNCTYPE(HCERTSTORE, POINTER(CRYPT_DATA_BLOB), LPCWSTR, DWORD)
PFXImportCertStoreParams = ((1, 'pPFX'), (1, 'szPassword'), (1, 'dwFlags'))



CryptGenKeyPrototype = WINFUNCTYPE(BOOL, HCRYPTPROV, ALG_ID, DWORD, POINTER(HCRYPTKEY))
CryptGenKeyParams = ((1, 'hProv'), (1, 'Algid'), (1, 'dwFlags'), (1, 'phKey'))



CryptDestroyKeyPrototype = WINFUNCTYPE(BOOL, HCRYPTKEY)
CryptDestroyKeyParams = ((1, 'hKey'),)



CryptAcquireContextAPrototype = WINFUNCTYPE(BOOL, POINTER(HCRYPTPROV), LPCSTR, LPCSTR, DWORD, DWORD)
CryptAcquireContextAParams = ((1, 'phProv'), (1, 'pszContainer'), (1, 'pszProvider'), (1, 'dwProvType'), (1, 'dwFlags'))



CryptAcquireContextWPrototype = WINFUNCTYPE(BOOL, POINTER(HCRYPTPROV), LPWSTR, LPWSTR, DWORD, DWORD)
CryptAcquireContextWParams = ((1, 'phProv'), (1, 'pszContainer'), (1, 'pszProvider'), (1, 'dwProvType'), (1, 'dwFlags'))



CryptReleaseContextPrototype = WINFUNCTYPE(BOOL, HCRYPTPROV, DWORD)
CryptReleaseContextParams = ((1, 'hProv'), (1, 'dwFlags'))



CryptCreateHashPrototype = WINFUNCTYPE(BOOL, HCRYPTPROV, ALG_ID, HCRYPTKEY, DWORD, POINTER(HCRYPTHASH))
CryptCreateHashParams = ((1, 'hProv'), (1, 'Algid'), (1, 'hKey'), (1, 'dwFlags'), (1, 'phHash'))



CryptHashDataPrototype = WINFUNCTYPE(BOOL, HCRYPTHASH, POINTER(BYTE), DWORD, DWORD)
CryptHashDataParams = ((1, 'hHash'), (1, 'pbData'), (1, 'dwDataLen'), (1, 'dwFlags'))



CryptGetHashParamPrototype = WINFUNCTYPE(BOOL, HCRYPTHASH, DWORD, POINTER(BYTE), POINTER(DWORD), DWORD)
CryptGetHashParamParams = ((1, 'hHash'), (1, 'dwParam'), (1, 'pbData'), (1, 'pdwDataLen'), (1, 'dwFlags'))



CryptVerifySignatureAPrototype = WINFUNCTYPE(BOOL, HCRYPTHASH, POINTER(BYTE), DWORD, HCRYPTKEY, LPCSTR, DWORD)
CryptVerifySignatureAParams = ((1, 'hHash'), (1, 'pbSignature'), (1, 'dwSigLen'), (1, 'hPubKey'), (1, 'szDescription'), (1, 'dwFlags'))



CryptVerifySignatureWPrototype = WINFUNCTYPE(BOOL, HCRYPTHASH, POINTER(BYTE), DWORD, HCRYPTKEY, LPCWSTR, DWORD)
CryptVerifySignatureWParams = ((1, 'hHash'), (1, 'pbSignature'), (1, 'dwSigLen'), (1, 'hPubKey'), (1, 'szDescription'), (1, 'dwFlags'))



CryptSignHashAPrototype = WINFUNCTYPE(BOOL, HCRYPTHASH, DWORD, LPCSTR, DWORD, POINTER(BYTE), POINTER(DWORD))
CryptSignHashAParams = ((1, 'hHash'), (1, 'dwKeySpec'), (1, 'szDescription'), (1, 'dwFlags'), (1, 'pbSignature'), (1, 'pdwSigLen'))



CryptSignHashWPrototype = WINFUNCTYPE(BOOL, HCRYPTHASH, DWORD, LPCWSTR, DWORD, POINTER(BYTE), POINTER(DWORD))
CryptSignHashWParams = ((1, 'hHash'), (1, 'dwKeySpec'), (1, 'szDescription'), (1, 'dwFlags'), (1, 'pbSignature'), (1, 'pdwSigLen'))



CryptDestroyHashPrototype = WINFUNCTYPE(BOOL, HCRYPTHASH)
CryptDestroyHashParams = ((1, 'hHash'),)



CryptEncryptPrototype = WINFUNCTYPE(BOOL, HCRYPTKEY, HCRYPTHASH, BOOL, DWORD, POINTER(BYTE), POINTER(DWORD), DWORD)
CryptEncryptParams = ((1, 'hKey'), (1, 'hHash'), (1, 'Final'), (1, 'dwFlags'), (1, 'pbData'), (1, 'pdwDataLen'), (1, 'dwBufLen'))



CryptDecryptPrototype = WINFUNCTYPE(BOOL, HCRYPTKEY, HCRYPTHASH, BOOL, DWORD, POINTER(BYTE), POINTER(DWORD))
CryptDecryptParams = ((1, 'hKey'), (1, 'hHash'), (1, 'Final'), (1, 'dwFlags'), (1, 'pbData'), (1, 'pdwDataLen'))



CryptDeriveKeyPrototype = WINFUNCTYPE(BOOL, HCRYPTPROV, ALG_ID, HCRYPTHASH, DWORD, POINTER(HCRYPTKEY))
CryptDeriveKeyParams = ((1, 'hProv'), (1, 'Algid'), (1, 'hBaseData'), (1, 'dwFlags'), (1, 'phKey'))



CryptExportKeyPrototype = WINFUNCTYPE(BOOL, HCRYPTKEY, HCRYPTKEY, DWORD, DWORD, POINTER(BYTE), POINTER(DWORD))
CryptExportKeyParams = ((1, 'hKey'), (1, 'hExpKey'), (1, 'dwBlobType'), (1, 'dwFlags'), (1, 'pbData'), (1, 'pdwDataLen'))



CryptImportKeyPrototype = WINFUNCTYPE(BOOL, HCRYPTPROV, POINTER(BYTE), DWORD, HCRYPTKEY, DWORD, POINTER(HCRYPTKEY))
CryptImportKeyParams = ((1, 'hProv'), (1, 'pbData'), (1, 'dwDataLen'), (1, 'hPubKey'), (1, 'dwFlags'), (1, 'phKey'))



CertGetCertificateContextPropertyPrototype = WINFUNCTYPE(BOOL, PCCERT_CONTEXT, DWORD, PVOID, POINTER(DWORD))
CertGetCertificateContextPropertyParams = ((1, 'pCertContext'), (1, 'dwPropId'), (1, 'pvData'), (1, 'pcbData'))



CertEnumCertificateContextPropertiesPrototype = WINFUNCTYPE(DWORD, PCCERT_CONTEXT, DWORD)
CertEnumCertificateContextPropertiesParams = ((1, 'pCertContext'), (1, 'dwPropId'))



CryptEncryptMessagePrototype = WINFUNCTYPE(BOOL, PCRYPT_ENCRYPT_MESSAGE_PARA, DWORD, POINTER(PCCERT_CONTEXT), POINTER(BYTE), DWORD, POINTER(BYTE), POINTER(DWORD))
CryptEncryptMessageParams = ((1, 'pEncryptPara'), (1, 'cRecipientCert'), (1, 'rgpRecipientCert'), (1, 'pbToBeEncrypted'), (1, 'cbToBeEncrypted'), (1, 'pbEncryptedBlob'), (1, 'pcbEncryptedBlob'))



CryptDecryptMessagePrototype = WINFUNCTYPE(BOOL, PCRYPT_DECRYPT_MESSAGE_PARA, POINTER(BYTE), DWORD, POINTER(BYTE), POINTER(DWORD), POINTER(PCCERT_CONTEXT))
CryptDecryptMessageParams = ((1, 'pDecryptPara'), (1, 'pbEncryptedBlob'), (1, 'cbEncryptedBlob'), (1, 'pbDecrypted'), (1, 'pcbDecrypted'), (1, 'ppXchgCert'))



CryptAcquireCertificatePrivateKeyPrototype = WINFUNCTYPE(BOOL, PCCERT_CONTEXT, DWORD, PVOID, POINTER(HCRYPTPROV_OR_NCRYPT_KEY_HANDLE), POINTER(DWORD), POINTER(BOOL))
CryptAcquireCertificatePrivateKeyParams = ((1, 'pCert'), (1, 'dwFlags'), (1, 'pvParameters'), (1, 'phCryptProvOrNCryptKey'), (1, 'pdwKeySpec'), (1, 'pfCallerFreeProvOrNCryptKey'))



CertDuplicateCertificateContextPrototype = WINFUNCTYPE(PCCERT_CONTEXT, PCCERT_CONTEXT)
CertDuplicateCertificateContextParams = ((1, 'pCertContext'),)



CertEnumCertificatesInStorePrototype = WINFUNCTYPE(PCCERT_CONTEXT, HCERTSTORE, PCCERT_CONTEXT)
CertEnumCertificatesInStoreParams = ((1, 'hCertStore'), (1, 'pPrevCertContext'))



CryptEncodeObjectExPrototype = WINFUNCTYPE(BOOL, DWORD, LPCSTR, PVOID, DWORD, PCRYPT_ENCODE_PARA, PVOID, POINTER(DWORD))
CryptEncodeObjectExParams = ((1, 'dwCertEncodingType'), (1, 'lpszStructType'), (1, 'pvStructInfo'), (1, 'dwFlags'), (1, 'pEncodePara'), (1, 'pvEncoded'), (1, 'pcbEncoded'))



CertCreateCertificateContextPrototype = WINFUNCTYPE(PCCERT_CONTEXT, DWORD, POINTER(BYTE), DWORD)
CertCreateCertificateContextParams = ((1, 'dwCertEncodingType'), (1, 'pbCertEncoded'), (1, 'cbCertEncoded'))



CertCompareCertificatePrototype = WINFUNCTYPE(BOOL, DWORD, PCERT_INFO, PCERT_INFO)
CertCompareCertificateParams = ((1, 'dwCertEncodingType'), (1, 'pCertId1'), (1, 'pCertId2'))



CertEnumCTLsInStorePrototype = WINFUNCTYPE(PCCTL_CONTEXT, HCERTSTORE, PCCTL_CONTEXT)
CertEnumCTLsInStoreParams = ((1, 'hCertStore'), (1, 'pPrevCtlContext'))



CertDuplicateCTLContextPrototype = WINFUNCTYPE(PCCTL_CONTEXT, PCCTL_CONTEXT)
CertDuplicateCTLContextParams = ((1, 'pCtlContext'),)



CertFreeCTLContextPrototype = WINFUNCTYPE(BOOL, PCCTL_CONTEXT)
CertFreeCTLContextParams = ((1, 'pCtlContext'),)



CryptUIDlgViewContextPrototype = WINFUNCTYPE(BOOL, DWORD, PVOID, HWND, LPCWSTR, DWORD, PVOID)
CryptUIDlgViewContextParams = ((1, 'dwContextType'), (1, 'pvContext'), (1, 'hwnd'), (1, 'pwszTitle'), (1, 'dwFlags'), (1, 'pvReserved'))



CryptMsgVerifyCountersignatureEncodedPrototype = WINFUNCTYPE(BOOL, HCRYPTPROV_LEGACY, DWORD, PBYTE, DWORD, PBYTE, DWORD, PCERT_INFO)
CryptMsgVerifyCountersignatureEncodedParams = ((1, 'hCryptProv'), (1, 'dwEncodingType'), (1, 'pbSignerInfo'), (1, 'cbSignerInfo'), (1, 'pbSignerInfoCountersignature'), (1, 'cbSignerInfoCountersignature'), (1, 'pciCountersigner'))



CryptMsgVerifyCountersignatureEncodedExPrototype = WINFUNCTYPE(BOOL, HCRYPTPROV_LEGACY, DWORD, PBYTE, DWORD, PBYTE, DWORD, DWORD, PVOID, DWORD, PVOID)
CryptMsgVerifyCountersignatureEncodedExParams = ((1, 'hCryptProv'), (1, 'dwEncodingType'), (1, 'pbSignerInfo'), (1, 'cbSignerInfo'), (1, 'pbSignerInfoCountersignature'), (1, 'cbSignerInfoCountersignature'), (1, 'dwSignerType'), (1, 'pvSigner'), (1, 'dwFlags'), (1, 'pvExtra'))



CryptHashCertificatePrototype = WINFUNCTYPE(BOOL, HCRYPTPROV_LEGACY, ALG_ID, DWORD, POINTER(BYTE), DWORD, POINTER(BYTE), POINTER(DWORD))
CryptHashCertificateParams = ((1, 'hCryptProv'), (1, 'Algid'), (1, 'dwFlags'), (1, 'pbEncoded'), (1, 'cbEncoded'), (1, 'pbComputedHash'), (1, 'pcbComputedHash'))



CryptSignMessagePrototype = WINFUNCTYPE(BOOL, PCRYPT_SIGN_MESSAGE_PARA, BOOL, DWORD, POINTER(PBYTE), POINTER(DWORD), POINTER(BYTE), POINTER(DWORD))
CryptSignMessageParams = ((1, 'pSignPara'), (1, 'fDetachedSignature'), (1, 'cToBeSigned'), (1, 'rgpbToBeSigned'), (1, 'rgcbToBeSigned'), (1, 'pbSignedBlob'), (1, 'pcbSignedBlob'))



CryptSignAndEncryptMessagePrototype = WINFUNCTYPE(BOOL, PCRYPT_SIGN_MESSAGE_PARA, PCRYPT_ENCRYPT_MESSAGE_PARA, DWORD, POINTER(PCCERT_CONTEXT), POINTER(BYTE), DWORD, POINTER(BYTE), POINTER(DWORD))
CryptSignAndEncryptMessageParams = ((1, 'pSignPara'), (1, 'pEncryptPara'), (1, 'cRecipientCert'), (1, 'rgpRecipientCert'), (1, 'pbToBeSignedAndEncrypted'), (1, 'cbToBeSignedAndEncrypted'), (1, 'pbSignedAndEncryptedBlob'), (1, 'pcbSignedAndEncryptedBlob'))



CryptVerifyMessageSignaturePrototype = WINFUNCTYPE(BOOL, PCRYPT_VERIFY_MESSAGE_PARA, DWORD, POINTER(BYTE), DWORD, POINTER(BYTE), POINTER(DWORD), POINTER(PCCERT_CONTEXT))
CryptVerifyMessageSignatureParams = ((1, 'pVerifyPara'), (1, 'dwSignerIndex'), (1, 'pbSignedBlob'), (1, 'cbSignedBlob'), (1, 'pbDecoded'), (1, 'pcbDecoded'), (1, 'ppSignerCert'))



CryptVerifyMessageSignatureWithKeyPrototype = WINFUNCTYPE(BOOL, PCRYPT_KEY_VERIFY_MESSAGE_PARA, PCERT_PUBLIC_KEY_INFO, POINTER(BYTE), DWORD, POINTER(BYTE), POINTER(DWORD))
CryptVerifyMessageSignatureWithKeyParams = ((1, 'pVerifyPara'), (1, 'pPublicKeyInfo'), (1, 'pbSignedBlob'), (1, 'cbSignedBlob'), (1, 'pbDecoded'), (1, 'pcbDecoded'))



CryptVerifyMessageHashPrototype = WINFUNCTYPE(BOOL, PCRYPT_HASH_MESSAGE_PARA, POINTER(BYTE), DWORD, POINTER(BYTE), POINTER(DWORD), POINTER(BYTE), POINTER(DWORD))
CryptVerifyMessageHashParams = ((1, 'pHashPara'), (1, 'pbHashedBlob'), (1, 'cbHashedBlob'), (1, 'pbToBeHashed'), (1, 'pcbToBeHashed'), (1, 'pbComputedHash'), (1, 'pcbComputedHash'))



PfnCryptGetSignerCertificatePrototype = WINFUNCTYPE(PCCERT_CONTEXT, PVOID, DWORD, PCERT_INFO, HCERTSTORE)
PfnCryptGetSignerCertificateParams = ((1, 'pvGetArg'), (1, 'dwCertEncodingType'), (1, 'pSignerId'), (1, 'hMsgCertStore'))



CryptEncryptPrototype = WINFUNCTYPE(BOOL, HCRYPTKEY, HCRYPTHASH, BOOL, DWORD, POINTER(BYTE), POINTER(DWORD), DWORD)
CryptEncryptParams = ((1, 'hKey'), (1, 'hHash'), (1, 'Final'), (1, 'dwFlags'), (1, 'pbData'), (1, 'pdwDataLen'), (1, 'dwBufLen'))



CryptDecryptPrototype = WINFUNCTYPE(BOOL, HCRYPTKEY, HCRYPTHASH, BOOL, DWORD, POINTER(BYTE), POINTER(DWORD))
CryptDecryptParams = ((1, 'hKey'), (1, 'hHash'), (1, 'Final'), (1, 'dwFlags'), (1, 'pbData'), (1, 'pdwDataLen'))



CryptMsgOpenToEncodePrototype = WINFUNCTYPE(HCRYPTMSG, DWORD, DWORD, DWORD, PVOID, LPSTR, PCMSG_STREAM_INFO)
CryptMsgOpenToEncodeParams = ((1, 'dwMsgEncodingType'), (1, 'dwFlags'), (1, 'dwMsgType'), (1, 'pvMsgEncodeInfo'), (1, 'pszInnerContentObjID'), (1, 'pStreamInfo'))



CryptMsgOpenToDecodePrototype = WINFUNCTYPE(HCRYPTMSG, DWORD, DWORD, DWORD, HCRYPTPROV_LEGACY, PCERT_INFO, PCMSG_STREAM_INFO)
CryptMsgOpenToDecodeParams = ((1, 'dwMsgEncodingType'), (1, 'dwFlags'), (1, 'dwMsgType'), (1, 'hCryptProv'), (1, 'pRecipientInfo'), (1, 'pStreamInfo'))



CryptMsgUpdatePrototype = WINFUNCTYPE(BOOL, HCRYPTMSG, POINTER(BYTE), DWORD, BOOL)
CryptMsgUpdateParams = ((1, 'hCryptMsg'), (1, 'pbData'), (1, 'cbData'), (1, 'fFinal'))



CryptMsgControlPrototype = WINFUNCTYPE(BOOL, HCRYPTMSG, DWORD, DWORD, PVOID)
CryptMsgControlParams = ((1, 'hCryptMsg'), (1, 'dwFlags'), (1, 'dwCtrlType'), (1, 'pvCtrlPara'))



CryptMsgClosePrototype = WINFUNCTYPE(BOOL, HCRYPTMSG)
CryptMsgCloseParams = ((1, 'hCryptMsg'),)



CryptEnumOIDFunctionPrototype = WINFUNCTYPE(BOOL, DWORD, LPCSTR, LPCSTR, DWORD, PVOID, PFN_CRYPT_ENUM_OID_FUNC)
CryptEnumOIDFunctionParams = ((1, 'dwEncodingType'), (1, 'pszFuncName'), (1, 'pszOID'), (1, 'dwFlags'), (1, 'pvArg'), (1, 'pfnEnumOIDFunc'))



CryptGetOIDFunctionValuePrototype = WINFUNCTYPE(BOOL, DWORD, LPCSTR, LPCSTR, LPCWSTR, POINTER(DWORD), POINTER(BYTE), POINTER(DWORD))
CryptGetOIDFunctionValueParams = ((1, 'dwEncodingType'), (1, 'pszFuncName'), (1, 'pszOID'), (1, 'pwszValueName'), (1, 'pdwValueType'), (1, 'pbValueData'), (1, 'pcbValueData'))



CertCloseStorePrototype = WINFUNCTYPE(BOOL, HCERTSTORE, DWORD)
CertCloseStoreParams = ((1, 'hCertStore'), (1, 'dwFlags'))



OpenVirtualDiskPrototype = WINFUNCTYPE(DWORD, PVIRTUAL_STORAGE_TYPE, PCWSTR, VIRTUAL_DISK_ACCESS_MASK, OPEN_VIRTUAL_DISK_FLAG, POPEN_VIRTUAL_DISK_PARAMETERS, PHANDLE)
OpenVirtualDiskParams = ((1, 'VirtualStorageType'), (1, 'Path'), (1, 'VirtualDiskAccessMask'), (1, 'Flags'), (1, 'Parameters'), (1, 'Handle'))



AttachVirtualDiskPrototype = WINFUNCTYPE(DWORD, HANDLE, PSECURITY_DESCRIPTOR, ATTACH_VIRTUAL_DISK_FLAG, ULONG, PATTACH_VIRTUAL_DISK_PARAMETERS, LPOVERLAPPED)
AttachVirtualDiskParams = ((1, 'VirtualDiskHandle'), (1, 'SecurityDescriptor'), (1, 'Flags'), (1, 'ProviderSpecificFlags'), (1, 'Parameters'), (1, 'Overlapped'))



CryptProtectDataPrototype = WINFUNCTYPE(BOOL, POINTER(DATA_BLOB), LPCWSTR, POINTER(DATA_BLOB), PVOID, POINTER(CRYPTPROTECT_PROMPTSTRUCT), DWORD, POINTER(DATA_BLOB))
CryptProtectDataParams = ((1, 'pDataIn'), (1, 'szDataDescr'), (1, 'pOptionalEntropy'), (1, 'pvReserved'), (1, 'pPromptStruct'), (1, 'dwFlags'), (1, 'pDataOut'))



CryptUnprotectDataPrototype = WINFUNCTYPE(BOOL, POINTER(DATA_BLOB), POINTER(LPWSTR), POINTER(DATA_BLOB), PVOID, POINTER(CRYPTPROTECT_PROMPTSTRUCT), DWORD, POINTER(DATA_BLOB))
CryptUnprotectDataParams = ((1, 'pDataIn'), (1, 'ppszDataDescr'), (1, 'pOptionalEntropy'), (1, 'pvReserved'), (1, 'pPromptStruct'), (1, 'dwFlags'), (1, 'pDataOut'))



CryptProtectMemoryPrototype = WINFUNCTYPE(BOOL, LPVOID, DWORD, DWORD)
CryptProtectMemoryParams = ((1, 'pDataIn'), (1, 'cbDataIn'), (1, 'dwFlags'))



CryptUnprotectMemoryPrototype = WINFUNCTYPE(BOOL, LPVOID, DWORD, DWORD)
CryptUnprotectMemoryParams = ((1, 'pDataIn'), (1, 'cbDataIn'), (1, 'dwFlags'))



EnumerateTraceGuidsExPrototype = WINFUNCTYPE(ULONG, TRACE_QUERY_INFO_CLASS, PVOID, ULONG, PVOID, ULONG, PULONG)
EnumerateTraceGuidsExParams = ((1, 'TraceQueryInfoClass'), (1, 'InBuffer'), (1, 'InBufferSize'), (1, 'OutBuffer'), (1, 'OutBufferSize'), (1, 'ReturnLength'))



QueryAllTracesAPrototype = WINFUNCTYPE(ULONG, POINTER(PEVENT_TRACE_PROPERTIES), ULONG, PULONG)
QueryAllTracesAParams = ((1, 'PropertyArray'), (1, 'PropertyArrayCount'), (1, 'SessionCount'))



QueryAllTracesWPrototype = WINFUNCTYPE(ULONG, POINTER(PEVENT_TRACE_PROPERTIES), ULONG, PULONG)
QueryAllTracesWParams = ((1, 'PropertyArray'), (1, 'PropertyArrayCount'), (1, 'SessionCount'))



OpenTraceAPrototype = WINFUNCTYPE(TRACEHANDLE, PEVENT_TRACE_LOGFILEA)
OpenTraceAParams = ((1, 'Logfile'),)



OpenTraceWPrototype = WINFUNCTYPE(TRACEHANDLE, PEVENT_TRACE_LOGFILEW)
OpenTraceWParams = ((1, 'Logfile'),)



StartTraceAPrototype = WINFUNCTYPE(ULONG, PTRACEHANDLE, LPCSTR, PEVENT_TRACE_PROPERTIES)
StartTraceAParams = ((1, 'TraceHandle'), (1, 'InstanceName'), (1, 'Properties'))



StartTraceWPrototype = WINFUNCTYPE(ULONG, PTRACEHANDLE, LPCWSTR, PEVENT_TRACE_PROPERTIES)
StartTraceWParams = ((1, 'TraceHandle'), (1, 'InstanceName'), (1, 'Properties'))



StopTraceAPrototype = WINFUNCTYPE(ULONG, TRACEHANDLE, LPCSTR, PEVENT_TRACE_PROPERTIES)
StopTraceAParams = ((1, 'TraceHandle'), (1, 'InstanceName'), (1, 'Properties'))



StopTraceWPrototype = WINFUNCTYPE(ULONG, TRACEHANDLE, LPCWSTR, PEVENT_TRACE_PROPERTIES)
StopTraceWParams = ((1, 'TraceHandle'), (1, 'InstanceName'), (1, 'Properties'))



ControlTraceAPrototype = WINFUNCTYPE(ULONG, TRACEHANDLE, LPCSTR, PEVENT_TRACE_PROPERTIES, ULONG)
ControlTraceAParams = ((1, 'TraceHandle'), (1, 'InstanceName'), (1, 'Properties'), (1, 'ControlCode'))



ControlTraceWPrototype = WINFUNCTYPE(ULONG, TRACEHANDLE, LPCWSTR, PEVENT_TRACE_PROPERTIES, ULONG)
ControlTraceWParams = ((1, 'TraceHandle'), (1, 'InstanceName'), (1, 'Properties'), (1, 'ControlCode'))



ProcessTracePrototype = WINFUNCTYPE(ULONG, PTRACEHANDLE, ULONG, LPFILETIME, LPFILETIME)
ProcessTraceParams = ((1, 'HandleArray'), (1, 'HandleCount'), (1, 'StartTime'), (1, 'EndTime'))



EnableTracePrototype = WINFUNCTYPE(ULONG, ULONG, ULONG, ULONG, LPCGUID, TRACEHANDLE)
EnableTraceParams = ((1, 'Enable'), (1, 'EnableFlag'), (1, 'EnableLevel'), (1, 'ControlGuid'), (1, 'SessionHandle'))



EnableTraceExPrototype = WINFUNCTYPE(ULONG, LPCGUID, LPCGUID, TRACEHANDLE, ULONG, UCHAR, ULONGLONG, ULONGLONG, ULONG, PEVENT_FILTER_DESCRIPTOR)
EnableTraceExParams = ((1, 'ProviderId'), (1, 'SourceId'), (1, 'TraceHandle'), (1, 'IsEnabled'), (1, 'Level'), (1, 'MatchAnyKeyword'), (1, 'MatchAllKeyword'), (1, 'EnableProperty'), (1, 'EnableFilterDesc'))



EnableTraceEx2Prototype = WINFUNCTYPE(ULONG, TRACEHANDLE, LPCGUID, ULONG, UCHAR, ULONGLONG, ULONGLONG, ULONG, PENABLE_TRACE_PARAMETERS)
EnableTraceEx2Params = ((1, 'TraceHandle'), (1, 'ProviderId'), (1, 'ControlCode'), (1, 'Level'), (1, 'MatchAnyKeyword'), (1, 'MatchAllKeyword'), (1, 'Timeout'), (1, 'EnableParameters'))



TraceQueryInformationPrototype = WINFUNCTYPE(ULONG, TRACEHANDLE, TRACE_QUERY_INFO_CLASS, PVOID, ULONG, PULONG)
TraceQueryInformationParams = ((1, 'SessionHandle'), (1, 'InformationClass'), (1, 'TraceInformation'), (1, 'InformationLength'), (1, 'ReturnLength'))



TraceSetInformationPrototype = WINFUNCTYPE(ULONG, TRACEHANDLE, TRACE_INFO_CLASS, PVOID, ULONG)
TraceSetInformationParams = ((1, 'SessionHandle'), (1, 'InformationClass'), (1, 'TraceInformation'), (1, 'InformationLength'))



RegisterTraceGuidsWPrototype = WINFUNCTYPE(ULONG, PVOID, PVOID, LPCGUID, ULONG, PTRACE_GUID_REGISTRATION, LPCWSTR, LPCWSTR, PTRACEHANDLE)
RegisterTraceGuidsWParams = ((1, 'RequestAddress'), (1, 'RequestContext'), (1, 'ControlGuid'), (1, 'GuidCount'), (1, 'TraceGuidReg'), (1, 'MofImagePath'), (1, 'MofResourceName'), (1, 'RegistrationHandle'))



RegisterTraceGuidsAPrototype = WINFUNCTYPE(ULONG, PVOID, PVOID, LPCGUID, ULONG, PTRACE_GUID_REGISTRATION, LPCSTR, LPCSTR, PTRACEHANDLE)
RegisterTraceGuidsAParams = ((1, 'RequestAddress'), (1, 'RequestContext'), (1, 'ControlGuid'), (1, 'GuidCount'), (1, 'TraceGuidReg'), (1, 'MofImagePath'), (1, 'MofResourceName'), (1, 'RegistrationHandle'))



TraceEventPrototype = WINFUNCTYPE(ULONG, TRACEHANDLE, PEVENT_TRACE_HEADER)
TraceEventParams = ((1, 'SessionHandle'), (1, 'EventTrace'))



GetTraceLoggerHandlePrototype = WINFUNCTYPE(TRACEHANDLE, PVOID)
GetTraceLoggerHandleParams = ((1, 'Buffer'),)



OpenEventLogAPrototype = WINFUNCTYPE(HANDLE, LPCSTR, LPCSTR)
OpenEventLogAParams = ((1, 'lpUNCServerName'), (1, 'lpSourceName'))



OpenEventLogWPrototype = WINFUNCTYPE(HANDLE, LPWSTR, LPWSTR)
OpenEventLogWParams = ((1, 'lpUNCServerName'), (1, 'lpSourceName'))



OpenBackupEventLogAPrototype = WINFUNCTYPE(HANDLE, LPCSTR, LPCSTR)
OpenBackupEventLogAParams = ((1, 'lpUNCServerName'), (1, 'lpSourceName'))



OpenBackupEventLogWPrototype = WINFUNCTYPE(HANDLE, LPWSTR, LPWSTR)
OpenBackupEventLogWParams = ((1, 'lpUNCServerName'), (1, 'lpSourceName'))



EvtOpenSessionPrototype = WINFUNCTYPE(EVT_HANDLE, EVT_LOGIN_CLASS, PVOID, DWORD, DWORD)
EvtOpenSessionParams = ((1, 'LoginClass'), (1, 'Login'), (1, 'Timeout'), (1, 'Flags'))



ReadEventLogAPrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD, DWORD, LPVOID, DWORD, POINTER(DWORD), POINTER(DWORD))
ReadEventLogAParams = ((1, 'hEventLog'), (1, 'dwReadFlags'), (1, 'dwRecordOffset'), (1, 'lpBuffer'), (1, 'nNumberOfBytesToRead'), (1, 'pnBytesRead'), (1, 'pnMinNumberOfBytesNeeded'))



ReadEventLogWPrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD, DWORD, LPVOID, DWORD, POINTER(DWORD), POINTER(DWORD))
ReadEventLogWParams = ((1, 'hEventLog'), (1, 'dwReadFlags'), (1, 'dwRecordOffset'), (1, 'lpBuffer'), (1, 'nNumberOfBytesToRead'), (1, 'pnBytesRead'), (1, 'pnMinNumberOfBytesNeeded'))



GetEventLogInformationPrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD, LPVOID, DWORD, LPDWORD)
GetEventLogInformationParams = ((1, 'hEventLog'), (1, 'dwInfoLevel'), (1, 'lpBuffer'), (1, 'cbBufSize'), (1, 'pcbBytesNeeded'))



GetNumberOfEventLogRecordsPrototype = WINFUNCTYPE(BOOL, HANDLE, PDWORD)
GetNumberOfEventLogRecordsParams = ((1, 'hEventLog'), (1, 'NumberOfRecords'))



CloseEventLogPrototype = WINFUNCTYPE(BOOL, HANDLE)
CloseEventLogParams = ((1, 'hEventLog'),)



EvtOpenLogPrototype = WINFUNCTYPE(EVT_HANDLE, EVT_HANDLE, LPCWSTR, DWORD)
EvtOpenLogParams = ((1, 'Session'), (1, 'Path'), (1, 'Flags'))



EvtQueryPrototype = WINFUNCTYPE(EVT_HANDLE, EVT_HANDLE, LPCWSTR, LPCWSTR, DWORD)
EvtQueryParams = ((1, 'Session'), (1, 'Path'), (1, 'Query'), (1, 'Flags'))



EvtNextPrototype = WINFUNCTYPE(BOOL, EVT_HANDLE, DWORD, POINTER(EVT_HANDLE), DWORD, DWORD, PDWORD)
EvtNextParams = ((1, 'ResultSet'), (1, 'EventArraySize'), (1, 'EventArray'), (1, 'Timeout'), (1, 'Flags'), (1, 'Returned'))



EvtCreateRenderContextPrototype = WINFUNCTYPE(EVT_HANDLE, DWORD, POINTER(LPCWSTR), DWORD)
EvtCreateRenderContextParams = ((1, 'ValuePathsCount'), (1, 'ValuePaths'), (1, 'Flags'))



EvtRenderPrototype = WINFUNCTYPE(BOOL, EVT_HANDLE, EVT_HANDLE, DWORD, DWORD, PVOID, PDWORD, PDWORD)
EvtRenderParams = ((1, 'Context'), (1, 'Fragment'), (1, 'Flags'), (1, 'BufferSize'), (1, 'Buffer'), (1, 'BufferUsed'), (1, 'PropertyCount'))



EvtClosePrototype = WINFUNCTYPE(BOOL, EVT_HANDLE)
EvtCloseParams = ((1, 'Object'),)



EvtOpenChannelEnumPrototype = WINFUNCTYPE(EVT_HANDLE, EVT_HANDLE, DWORD)
EvtOpenChannelEnumParams = ((1, 'Session'), (1, 'Flags'))



EvtNextChannelPathPrototype = WINFUNCTYPE(BOOL, EVT_HANDLE, DWORD, LPWSTR, PDWORD)
EvtNextChannelPathParams = ((1, 'ChannelEnum'), (1, 'ChannelPathBufferSize'), (1, 'ChannelPathBuffer'), (1, 'ChannelPathBufferUsed'))



EvtOpenPublisherEnumPrototype = WINFUNCTYPE(EVT_HANDLE, EVT_HANDLE, DWORD)
EvtOpenPublisherEnumParams = ((1, 'Session'), (1, 'Flags'))



EvtNextPublisherIdPrototype = WINFUNCTYPE(BOOL, EVT_HANDLE, DWORD, LPWSTR, PDWORD)
EvtNextPublisherIdParams = ((1, 'PublisherEnum'), (1, 'PublisherIdBufferSize'), (1, 'PublisherIdBuffer'), (1, 'PublisherIdBufferUsed'))



EvtGetLogInfoPrototype = WINFUNCTYPE(BOOL, EVT_HANDLE, EVT_LOG_PROPERTY_ID, DWORD, PEVT_VARIANT, PDWORD)
EvtGetLogInfoParams = ((1, 'Log'), (1, 'PropertyId'), (1, 'PropertyValueBufferSize'), (1, 'PropertyValueBuffer'), (1, 'PropertyValueBufferUsed'))



EvtOpenChannelConfigPrototype = WINFUNCTYPE(EVT_HANDLE, EVT_HANDLE, LPCWSTR, DWORD)
EvtOpenChannelConfigParams = ((1, 'Session'), (1, 'ChannelPath'), (1, 'Flags'))



EvtGetChannelConfigPropertyPrototype = WINFUNCTYPE(BOOL, EVT_HANDLE, EVT_CHANNEL_CONFIG_PROPERTY_ID, DWORD, DWORD, PEVT_VARIANT, PDWORD)
EvtGetChannelConfigPropertyParams = ((1, 'ChannelConfig'), (1, 'PropertyId'), (1, 'Flags'), (1, 'PropertyValueBufferSize'), (1, 'PropertyValueBuffer'), (1, 'PropertyValueBufferUsed'))



EvtOpenPublisherMetadataPrototype = WINFUNCTYPE(EVT_HANDLE, EVT_HANDLE, LPCWSTR, LPCWSTR, LCID, DWORD)
EvtOpenPublisherMetadataParams = ((1, 'Session'), (1, 'PublisherIdentity'), (1, 'LogFilePath'), (1, 'Locale'), (1, 'Flags'))



EvtOpenEventMetadataEnumPrototype = WINFUNCTYPE(EVT_HANDLE, EVT_HANDLE, DWORD)
EvtOpenEventMetadataEnumParams = ((1, 'PublisherMetadata'), (1, 'Flags'))



EvtNextEventMetadataPrototype = WINFUNCTYPE(EVT_HANDLE, EVT_HANDLE, DWORD)
EvtNextEventMetadataParams = ((1, 'EventMetadataEnum'), (1, 'Flags'))



EvtGetEventMetadataPropertyPrototype = WINFUNCTYPE(BOOL, EVT_HANDLE, EVT_EVENT_METADATA_PROPERTY_ID, DWORD, DWORD, PEVT_VARIANT, PDWORD)
EvtGetEventMetadataPropertyParams = ((1, 'EventMetadata'), (1, 'PropertyId'), (1, 'Flags'), (1, 'EventMetadataPropertyBufferSize'), (1, 'EventMetadataPropertyBuffer'), (1, 'EventMetadataPropertyBufferUsed'))



EvtGetPublisherMetadataPropertyPrototype = WINFUNCTYPE(BOOL, EVT_HANDLE, EVT_PUBLISHER_METADATA_PROPERTY_ID, DWORD, DWORD, PEVT_VARIANT, PDWORD)
EvtGetPublisherMetadataPropertyParams = ((1, 'PublisherMetadata'), (1, 'PropertyId'), (1, 'Flags'), (1, 'PublisherMetadataPropertyBufferSize'), (1, 'PublisherMetadataPropertyBuffer'), (1, 'PublisherMetadataPropertyBufferUsed'))



EvtGetObjectArraySizePrototype = WINFUNCTYPE(BOOL, EVT_OBJECT_ARRAY_PROPERTY_HANDLE, PDWORD)
EvtGetObjectArraySizeParams = ((1, 'ObjectArray'), (1, 'ObjectArraySize'))



EvtGetObjectArrayPropertyPrototype = WINFUNCTYPE(BOOL, EVT_OBJECT_ARRAY_PROPERTY_HANDLE, DWORD, DWORD, DWORD, DWORD, PEVT_VARIANT, PDWORD)
EvtGetObjectArrayPropertyParams = ((1, 'ObjectArray'), (1, 'PropertyId'), (1, 'ArrayIndex'), (1, 'Flags'), (1, 'PropertyValueBufferSize'), (1, 'PropertyValueBuffer'), (1, 'PropertyValueBufferUsed'))



EvtFormatMessagePrototype = WINFUNCTYPE(BOOL, EVT_HANDLE, EVT_HANDLE, DWORD, DWORD, PEVT_VARIANT, DWORD, DWORD, LPWSTR, PDWORD)
EvtFormatMessageParams = ((1, 'PublisherMetadata'), (1, 'Event'), (1, 'MessageId'), (1, 'ValueCount'), (1, 'Values'), (1, 'Flags'), (1, 'BufferSize'), (1, 'Buffer'), (1, 'BufferUsed'))



EvtSeekPrototype = WINFUNCTYPE(BOOL, EVT_HANDLE, LONGLONG, EVT_HANDLE, DWORD, DWORD)
EvtSeekParams = ((1, 'ResultSet'), (1, 'Position'), (1, 'Bookmark'), (1, 'Timeout'), (1, 'Flags'))



FindFirstFileAPrototype = WINFUNCTYPE(HANDLE, LPCSTR, LPWIN32_FIND_DATAA)
FindFirstFileAParams = ((1, 'lpFileName'), (1, 'lpFindFileData'))



FindFirstFileWPrototype = WINFUNCTYPE(HANDLE, LPCWSTR, LPWIN32_FIND_DATAW)
FindFirstFileWParams = ((1, 'lpFileName'), (1, 'lpFindFileData'))



FindNextFileAPrototype = WINFUNCTYPE(BOOL, HANDLE, LPWIN32_FIND_DATAA)
FindNextFileAParams = ((1, 'hFindFile'), (1, 'lpFindFileData'))



FindNextFileWPrototype = WINFUNCTYPE(BOOL, HANDLE, LPWIN32_FIND_DATAW)
FindNextFileWParams = ((1, 'hFindFile'), (1, 'lpFindFileData'))



FindClosePrototype = WINFUNCTYPE(BOOL, HANDLE)
FindCloseParams = ((1, 'hFindFile'),)



FindFirstChangeNotificationAPrototype = WINFUNCTYPE(HANDLE, LPCSTR, BOOL, DWORD)
FindFirstChangeNotificationAParams = ((1, 'lpPathName'), (1, 'bWatchSubtree'), (1, 'dwNotifyFilter'))



FindFirstChangeNotificationWPrototype = WINFUNCTYPE(HANDLE, LPCWSTR, BOOL, DWORD)
FindFirstChangeNotificationWParams = ((1, 'lpPathName'), (1, 'bWatchSubtree'), (1, 'dwNotifyFilter'))



FindNextChangeNotificationPrototype = WINFUNCTYPE(BOOL, HANDLE)
FindNextChangeNotificationParams = ((1, 'hChangeHandle'),)



FindCloseChangeNotificationPrototype = WINFUNCTYPE(BOOL, HANDLE)
FindCloseChangeNotificationParams = ((1, 'hChangeHandle'),)



FindNextChangeNotificationPrototype = WINFUNCTYPE(BOOL, HANDLE)
FindNextChangeNotificationParams = ((1, 'hChangeHandle'),)



ReadDirectoryChangesWPrototype = WINFUNCTYPE(BOOL, HANDLE, LPVOID, DWORD, BOOL, DWORD, LPDWORD, LPOVERLAPPED, LPOVERLAPPED_COMPLETION_ROUTINE)
ReadDirectoryChangesWParams = ((1, 'hDirectory'), (1, 'lpBuffer'), (1, 'nBufferLength'), (1, 'bWatchSubtree'), (1, 'dwNotifyFilter'), (1, 'lpBytesReturned'), (1, 'lpOverlapped'), (1, 'lpCompletionRoutine'))



ReadDirectoryChangesExWPrototype = WINFUNCTYPE(BOOL, HANDLE, LPVOID, DWORD, BOOL, DWORD, LPDWORD, LPOVERLAPPED, LPOVERLAPPED_COMPLETION_ROUTINE, READ_DIRECTORY_NOTIFY_INFORMATION_CLASS)
ReadDirectoryChangesExWParams = ((1, 'hDirectory'), (1, 'lpBuffer'), (1, 'nBufferLength'), (1, 'bWatchSubtree'), (1, 'dwNotifyFilter'), (1, 'lpBytesReturned'), (1, 'lpOverlapped'), (1, 'lpCompletionRoutine'), (1, 'ReadDirectoryNotifyInformationClass'))



HeapAllocPrototype = WINFUNCTYPE(LPVOID, HANDLE, DWORD, SIZE_T)
HeapAllocParams = ((1, 'hHeap'), (1, 'dwFlags'), (1, 'dwBytes'))



InternetCheckConnectionAPrototype = WINFUNCTYPE(BOOL, LPCSTR, DWORD, DWORD)
InternetCheckConnectionAParams = ((1, 'lpszUrl'), (1, 'dwFlags'), (1, 'dwReserved'))



InternetCheckConnectionWPrototype = WINFUNCTYPE(BOOL, LPCWSTR, DWORD, DWORD)
InternetCheckConnectionWParams = ((1, 'lpszUrl'), (1, 'dwFlags'), (1, 'dwReserved'))



InternetOpenAPrototype = WINFUNCTYPE(HINTERNET, LPCSTR, DWORD, LPCSTR, LPCSTR, DWORD)
InternetOpenAParams = ((1, 'lpszAgent'), (1, 'dwAccessType'), (1, 'lpszProxy'), (1, 'lpszProxyBypass'), (1, 'dwFlags'))



InternetOpenWPrototype = WINFUNCTYPE(HINTERNET, LPCWSTR, DWORD, LPCWSTR, LPCWSTR, DWORD)
InternetOpenWParams = ((1, 'lpszAgent'), (1, 'dwAccessType'), (1, 'lpszProxy'), (1, 'lpszProxyBypass'), (1, 'dwFlags'))



InternetOpenUrlAPrototype = WINFUNCTYPE(HINTERNET, HINTERNET, LPCSTR, LPCSTR, DWORD, DWORD, DWORD_PTR)
InternetOpenUrlAParams = ((1, 'hInternet'), (1, 'lpszUrl'), (1, 'lpszHeaders'), (1, 'dwHeadersLength'), (1, 'dwFlags'), (1, 'dwContext'))



InternetOpenUrlWPrototype = WINFUNCTYPE(HINTERNET, HINTERNET, LPCWSTR, LPCWSTR, DWORD, DWORD, DWORD_PTR)
InternetOpenUrlWParams = ((1, 'hInternet'), (1, 'lpszUrl'), (1, 'lpszHeaders'), (1, 'dwHeadersLength'), (1, 'dwFlags'), (1, 'dwContext'))



InternetConnectAPrototype = WINFUNCTYPE(HINTERNET, HINTERNET, LPCSTR, INTERNET_PORT, LPCSTR, LPCSTR, DWORD, DWORD, DWORD_PTR)
InternetConnectAParams = ((1, 'hInternet'), (1, 'lpszServerName'), (1, 'nServerPort'), (1, 'lpszUserName'), (1, 'lpszPassword'), (1, 'dwService'), (1, 'dwFlags'), (1, 'dwContext'))



InternetConnectWPrototype = WINFUNCTYPE(HINTERNET, HINTERNET, LPCWSTR, INTERNET_PORT, LPCWSTR, LPCWSTR, DWORD, DWORD, DWORD_PTR)
InternetConnectWParams = ((1, 'hInternet'), (1, 'lpszServerName'), (1, 'nServerPort'), (1, 'lpszUserName'), (1, 'lpszPassword'), (1, 'dwService'), (1, 'dwFlags'), (1, 'dwContext'))



HttpOpenRequestAPrototype = WINFUNCTYPE(HINTERNET, HINTERNET, LPCSTR, LPCSTR, LPCSTR, LPCSTR, POINTER(LPCSTR), DWORD, DWORD_PTR)
HttpOpenRequestAParams = ((1, 'hConnect'), (1, 'lpszVerb'), (1, 'lpszObjectName'), (1, 'lpszVersion'), (1, 'lpszReferrer'), (1, 'lplpszAcceptTypes'), (1, 'dwFlags'), (1, 'dwContext'))



HttpOpenRequestWPrototype = WINFUNCTYPE(HINTERNET, HINTERNET, LPCWSTR, LPCWSTR, LPCWSTR, LPCWSTR, POINTER(LPCWSTR), DWORD, DWORD_PTR)
HttpOpenRequestWParams = ((1, 'hConnect'), (1, 'lpszVerb'), (1, 'lpszObjectName'), (1, 'lpszVersion'), (1, 'lpszReferrer'), (1, 'lplpszAcceptTypes'), (1, 'dwFlags'), (1, 'dwContext'))



InternetSetOptionAPrototype = WINFUNCTYPE(BOOL, HINTERNET, DWORD, LPVOID, DWORD)
InternetSetOptionAParams = ((1, 'hInternet'), (1, 'dwOption'), (1, 'lpBuffer'), (1, 'dwBufferLength'))



InternetSetOptionWPrototype = WINFUNCTYPE(BOOL, HINTERNET, DWORD, LPVOID, DWORD)
InternetSetOptionWParams = ((1, 'hInternet'), (1, 'dwOption'), (1, 'lpBuffer'), (1, 'dwBufferLength'))



HttpSendRequestAPrototype = WINFUNCTYPE(BOOL, HINTERNET, LPCSTR, DWORD, LPVOID, DWORD)
HttpSendRequestAParams = ((1, 'hRequest'), (1, 'lpszHeaders'), (1, 'dwHeadersLength'), (1, 'lpOptional'), (1, 'dwOptionalLength'))



HttpSendRequestWPrototype = WINFUNCTYPE(BOOL, HINTERNET, LPCWSTR, DWORD, LPVOID, DWORD)
HttpSendRequestWParams = ((1, 'hRequest'), (1, 'lpszHeaders'), (1, 'dwHeadersLength'), (1, 'lpOptional'), (1, 'dwOptionalLength'))



InternetReadFilePrototype = WINFUNCTYPE(BOOL, HINTERNET, LPVOID, DWORD, LPDWORD)
InternetReadFileParams = ((1, 'hFile'), (1, 'lpBuffer'), (1, 'dwNumberOfBytesToRead'), (1, 'lpdwNumberOfBytesRead'))



InternetReadFileExAPrototype = WINFUNCTYPE(BOOL, HINTERNET, LPINTERNET_BUFFERSA, DWORD, DWORD_PTR)
InternetReadFileExAParams = ((1, 'hFile'), (1, 'lpBuffersOut'), (1, 'dwFlags'), (1, 'dwContext'))



InternetReadFileExWPrototype = WINFUNCTYPE(BOOL, HINTERNET, LPINTERNET_BUFFERSW, DWORD, DWORD_PTR)
InternetReadFileExWParams = ((1, 'hFile'), (1, 'lpBuffersOut'), (1, 'dwFlags'), (1, 'dwContext'))



HttpQueryInfoAPrototype = WINFUNCTYPE(BOOL, HINTERNET, DWORD, LPVOID, LPDWORD, LPDWORD)
HttpQueryInfoAParams = ((1, 'hRequest'), (1, 'dwInfoLevel'), (1, 'lpBuffer'), (1, 'lpdwBufferLength'), (1, 'lpdwIndex'))



HttpQueryInfoWPrototype = WINFUNCTYPE(BOOL, HINTERNET, DWORD, LPVOID, LPDWORD, LPDWORD)
HttpQueryInfoWParams = ((1, 'hRequest'), (1, 'dwInfoLevel'), (1, 'lpBuffer'), (1, 'lpdwBufferLength'), (1, 'lpdwIndex'))



HttpSendRequestAPrototype = WINFUNCTYPE(BOOL, HINTERNET, LPCSTR, DWORD, LPVOID, DWORD)
HttpSendRequestAParams = ((1, 'hRequest'), (1, 'lpszHeaders'), (1, 'dwHeadersLength'), (1, 'lpOptional'), (1, 'dwOptionalLength'))



HttpSendRequestWPrototype = WINFUNCTYPE(BOOL, HINTERNET, LPCWSTR, DWORD, LPVOID, DWORD)
HttpSendRequestWParams = ((1, 'hRequest'), (1, 'lpszHeaders'), (1, 'dwHeadersLength'), (1, 'lpOptional'), (1, 'dwOptionalLength'))



WinHttpOpenPrototype = WINFUNCTYPE(HINTERNET, LPCWSTR, DWORD, LPCWSTR, LPCWSTR, DWORD)
WinHttpOpenParams = ((1, 'pszAgentW'), (1, 'dwAccessType'), (1, 'pszProxyW'), (1, 'pszProxyBypassW'), (1, 'dwFlags'))



WinHttpCloseHandlePrototype = WINFUNCTYPE(BOOL, HINTERNET)
WinHttpCloseHandleParams = ((1, 'hInternet'),)



WinHttpConnectPrototype = WINFUNCTYPE(HINTERNET, HINTERNET, LPCWSTR, INTERNET_PORT, DWORD)
WinHttpConnectParams = ((1, 'hSession'), (1, 'pswzServerName'), (1, 'nServerPort'), (1, 'dwReserved'))



WinHttpQueryDataAvailablePrototype = WINFUNCTYPE(BOOL, HINTERNET, LPDWORD)
WinHttpQueryDataAvailableParams = ((1, 'hRequest'), (1, 'lpdwNumberOfBytesAvailable'))



WinHttpReadDataPrototype = WINFUNCTYPE(BOOL, HINTERNET, LPVOID, DWORD, LPDWORD)
WinHttpReadDataParams = ((1, 'hRequest'), (1, 'lpBuffer'), (1, 'dwNumberOfBytesToRead'), (1, 'lpdwNumberOfBytesRead'))



WinHttpOpenRequestPrototype = WINFUNCTYPE(HINTERNET, HINTERNET, LPCWSTR, LPCWSTR, LPCWSTR, LPCWSTR, POINTER(LPCWSTR), DWORD)
WinHttpOpenRequestParams = ((1, 'hConnect'), (1, 'pwszVerb'), (1, 'pwszObjectName'), (1, 'pwszVersion'), (1, 'pwszReferrer'), (1, 'ppwszAcceptTypes'), (1, 'dwFlags'))



WinHttpSendRequestPrototype = WINFUNCTYPE(BOOL, HINTERNET, LPCWSTR, DWORD, LPVOID, DWORD, DWORD, DWORD_PTR)
WinHttpSendRequestParams = ((1, 'hRequest'), (1, 'lpszHeaders'), (1, 'dwHeadersLength'), (1, 'lpOptional'), (1, 'dwOptionalLength'), (1, 'dwTotalLength'), (1, 'dwContext'))



WinHttpReceiveResponsePrototype = WINFUNCTYPE(BOOL, HINTERNET, LPVOID)
WinHttpReceiveResponseParams = ((1, 'hRequest'), (1, 'lpReserved'))



WinHttpAddRequestHeadersPrototype = WINFUNCTYPE(BOOL, HINTERNET, LPCWSTR, DWORD, DWORD)
WinHttpAddRequestHeadersParams = ((1, 'hRequest'), (1, 'lpszHeaders'), (1, 'dwHeadersLength'), (1, 'dwModifiers'))



WinHttpQueryHeadersPrototype = WINFUNCTYPE(BOOL, HINTERNET, DWORD, LPCWSTR, LPVOID, LPDWORD, LPDWORD)
WinHttpQueryHeadersParams = ((1, 'hRequest'), (1, 'dwInfoLevel'), (1, 'pwszName'), (1, 'lpBuffer'), (1, 'lpdwBufferLength'), (1, 'lpdwIndex'))



LsaOpenPolicyPrototype = WINFUNCTYPE(NTSTATUS, PLSA_UNICODE_STRING, PLSA_OBJECT_ATTRIBUTES, ACCESS_MASK, PLSA_HANDLE)
LsaOpenPolicyParams = ((1, 'SystemName'), (1, 'ObjectAttributes'), (1, 'DesiredAccess'), (1, 'PolicyHandle'))



LsaQueryInformationPolicyPrototype = WINFUNCTYPE(NTSTATUS, LSA_HANDLE, POLICY_INFORMATION_CLASS, POINTER(PVOID))
LsaQueryInformationPolicyParams = ((1, 'PolicyHandle'), (1, 'InformationClass'), (1, 'Buffer'))



LsaClosePrototype = WINFUNCTYPE(NTSTATUS, LSA_HANDLE)
LsaCloseParams = ((1, 'ObjectHandle'),)



LsaNtStatusToWinErrorPrototype = WINFUNCTYPE(ULONG, NTSTATUS)
LsaNtStatusToWinErrorParams = ((1, 'Status'),)



LsaLookupNamesPrototype = WINFUNCTYPE(NTSTATUS, LSA_HANDLE, ULONG, PLSA_UNICODE_STRING, POINTER(PLSA_REFERENCED_DOMAIN_LIST), POINTER(PLSA_TRANSLATED_SID))
LsaLookupNamesParams = ((1, 'PolicyHandle'), (1, 'Count'), (1, 'Names'), (1, 'ReferencedDomains'), (1, 'Sids'))



LsaLookupNames2Prototype = WINFUNCTYPE(NTSTATUS, LSA_HANDLE, ULONG, ULONG, PLSA_UNICODE_STRING, POINTER(PLSA_REFERENCED_DOMAIN_LIST), POINTER(PLSA_TRANSLATED_SID2))
LsaLookupNames2Params = ((1, 'PolicyHandle'), (1, 'Flags'), (1, 'Count'), (1, 'Names'), (1, 'ReferencedDomains'), (1, 'Sids'))



LsaLookupSidsPrototype = WINFUNCTYPE(NTSTATUS, LSA_HANDLE, ULONG, POINTER(PSID), POINTER(PLSA_REFERENCED_DOMAIN_LIST), POINTER(PLSA_TRANSLATED_NAME))
LsaLookupSidsParams = ((1, 'PolicyHandle'), (1, 'Count'), (1, 'Sids'), (1, 'ReferencedDomains'), (1, 'Names'))



LsaLookupSids2Prototype = WINFUNCTYPE(NTSTATUS, LSA_HANDLE, ULONG, ULONG, POINTER(PSID), POINTER(PLSA_REFERENCED_DOMAIN_LIST), POINTER(PLSA_TRANSLATED_NAME))
LsaLookupSids2Params = ((1, 'PolicyHandle'), (1, 'LookupOptions'), (1, 'Count'), (1, 'Sids'), (1, 'ReferencedDomains'), (1, 'Names'))



OpenFileMappingWPrototype = WINFUNCTYPE(HANDLE, DWORD, BOOL, LPCWSTR)
OpenFileMappingWParams = ((1, 'dwDesiredAccess'), (1, 'bInheritHandle'), (1, 'lpName'))



OpenFileMappingAPrototype = WINFUNCTYPE(HANDLE, DWORD, BOOL, LPCSTR)
OpenFileMappingAParams = ((1, 'dwDesiredAccess'), (1, 'bInheritHandle'), (1, 'lpName'))



UnmapViewOfFilePrototype = WINFUNCTYPE(BOOL, LPCVOID)
UnmapViewOfFileParams = ((1, 'lpBaseAddress'),)



NetLocalGroupGetMembersPrototype = WINFUNCTYPE(NET_API_STATUS, LPCWSTR, LPCWSTR, DWORD, POINTER(LPBYTE), DWORD, LPDWORD, LPDWORD, PDWORD_PTR)
NetLocalGroupGetMembersParams = ((1, 'servername'), (1, 'localgroupname'), (1, 'level'), (1, 'bufptr'), (1, 'prefmaxlen'), (1, 'entriesread'), (1, 'totalentries'), (1, 'resumehandle'))



NetQueryDisplayInformationPrototype = WINFUNCTYPE(NET_API_STATUS, LPCWSTR, DWORD, DWORD, DWORD, DWORD, LPDWORD, POINTER(PVOID))
NetQueryDisplayInformationParams = ((1, 'ServerName'), (1, 'Level'), (1, 'Index'), (1, 'EntriesRequested'), (1, 'PreferredMaximumLength'), (1, 'ReturnedEntryCount'), (1, 'SortedBuffer'))



NetUserEnumPrototype = WINFUNCTYPE(NET_API_STATUS, LPCWSTR, DWORD, DWORD, POINTER(LPBYTE), DWORD, LPDWORD, LPDWORD, PDWORD)
NetUserEnumParams = ((1, 'servername'), (1, 'level'), (1, 'filter'), (1, 'bufptr'), (1, 'prefmaxlen'), (1, 'entriesread'), (1, 'totalentries'), (1, 'resume_handle'))



NetGroupEnumPrototype = WINFUNCTYPE(NET_API_STATUS, LPCWSTR, DWORD, POINTER(LPBYTE), DWORD, LPDWORD, LPDWORD, PDWORD_PTR)
NetGroupEnumParams = ((1, 'servername'), (1, 'level'), (1, 'bufptr'), (1, 'prefmaxlen'), (1, 'entriesread'), (1, 'totalentries'), (1, 'resume_handle'))



NetGroupGetInfoPrototype = WINFUNCTYPE(NET_API_STATUS, LPCWSTR, LPCWSTR, DWORD, POINTER(LPBYTE))
NetGroupGetInfoParams = ((1, 'servername'), (1, 'groupname'), (1, 'level'), (1, 'bufptr'))



NetGroupGetUsersPrototype = WINFUNCTYPE(NET_API_STATUS, LPCWSTR, LPCWSTR, DWORD, POINTER(LPBYTE), DWORD, LPDWORD, LPDWORD, PDWORD_PTR)
NetGroupGetUsersParams = ((1, 'servername'), (1, 'groupname'), (1, 'level'), (1, 'bufptr'), (1, 'prefmaxlen'), (1, 'entriesread'), (1, 'totalentries'), (1, 'ResumeHandle'))



NetLocalGroupEnumPrototype = WINFUNCTYPE(NET_API_STATUS, LPCWSTR, DWORD, POINTER(LPBYTE), DWORD, LPDWORD, LPDWORD, PDWORD_PTR)
NetLocalGroupEnumParams = ((1, 'servername'), (1, 'level'), (1, 'bufptr'), (1, 'prefmaxlen'), (1, 'entriesread'), (1, 'totalentries'), (1, 'resumehandle'))



NetLocalGroupGetInfoPrototype = WINFUNCTYPE(NET_API_STATUS, LPCWSTR, LPCWSTR, DWORD, POINTER(LPBYTE))
NetLocalGroupGetInfoParams = ((1, 'servername'), (1, 'groupname'), (1, 'level'), (1, 'bufptr'))



NetLocalGroupGetMembersPrototype = WINFUNCTYPE(NET_API_STATUS, LPCWSTR, LPCWSTR, DWORD, POINTER(LPBYTE), DWORD, LPDWORD, LPDWORD, PDWORD_PTR)
NetLocalGroupGetMembersParams = ((1, 'servername'), (1, 'localgroupname'), (1, 'level'), (1, 'bufptr'), (1, 'prefmaxlen'), (1, 'entriesread'), (1, 'totalentries'), (1, 'resumehandle'))



NetLocalGroupGetInfoPrototype = WINFUNCTYPE(NET_API_STATUS, LPCWSTR, LPCWSTR, DWORD, POINTER(LPBYTE))
NetLocalGroupGetInfoParams = ((1, 'servername'), (1, 'groupname'), (1, 'level'), (1, 'bufptr'))



NetLocalGroupEnumPrototype = WINFUNCTYPE(NET_API_STATUS, LPCWSTR, DWORD, POINTER(LPBYTE), DWORD, LPDWORD, LPDWORD, PDWORD_PTR)
NetLocalGroupEnumParams = ((1, 'servername'), (1, 'level'), (1, 'bufptr'), (1, 'prefmaxlen'), (1, 'entriesread'), (1, 'totalentries'), (1, 'resumehandle'))



NetApiBufferFreePrototype = WINFUNCTYPE(NET_API_STATUS, LPVOID)
NetApiBufferFreeParams = ((1, 'Buffer'),)



GetIpNetTablePrototype = WINFUNCTYPE(ULONG, PMIB_IPNETTABLE, PULONG, BOOL)
GetIpNetTableParams = ((1, 'IpNetTable'), (1, 'SizePointer'), (1, 'Order'))



GetExtendedTcpTablePrototype = WINFUNCTYPE(DWORD, PVOID, PDWORD, BOOL, ULONG, TCP_TABLE_CLASS, ULONG)
GetExtendedTcpTableParams = ((1, 'pTcpTable'), (1, 'pdwSize'), (1, 'bOrder'), (1, 'ulAf'), (1, 'TableClass'), (1, 'Reserved'))



GetExtendedUdpTablePrototype = WINFUNCTYPE(DWORD, PVOID, PDWORD, BOOL, ULONG, UDP_TABLE_CLASS, ULONG)
GetExtendedUdpTableParams = ((1, 'pUdpTable'), (1, 'pdwSize'), (1, 'bOrder'), (1, 'ulAf'), (1, 'TableClass'), (1, 'Reserved'))



SetTcpEntryPrototype = WINFUNCTYPE(DWORD, PMIB_TCPROW)
SetTcpEntryParams = ((1, 'pTcpRow'),)



DnsGetCacheDataTablePrototype = WINFUNCTYPE(DWORD, POINTER(PDNS_CACHE_ENTRY))
DnsGetCacheDataTableParams = ((1, 'DnsEntries'),)



DnsFreePrototype = WINFUNCTYPE(VOID, PVOID, DNS_FREE_TYPE)
DnsFreeParams = ((1, 'pData'), (1, 'FreeType'))



DnsQuery_APrototype = WINFUNCTYPE(DNS_STATUS, PCSTR, WORD, DWORD, PVOID, POINTER(PDNS_RECORDA), POINTER(PVOID))
DnsQuery_AParams = ((1, 'pszName'), (1, 'wType'), (1, 'Options'), (1, 'pExtra'), (1, 'ppQueryResults'), (1, 'pReserved'))



DnsQuery_WPrototype = WINFUNCTYPE(DNS_STATUS, PCWSTR, WORD, DWORD, PVOID, POINTER(PDNS_RECORDW), POINTER(PVOID))
DnsQuery_WParams = ((1, 'pszName'), (1, 'wType'), (1, 'Options'), (1, 'pExtra'), (1, 'ppQueryResults'), (1, 'pReserved'))



DnsQueryExPrototype = WINFUNCTYPE(DNS_STATUS, PDNS_QUERY_REQUEST, PDNS_QUERY_RESULT, PDNS_QUERY_CANCEL)
DnsQueryExParams = ((1, 'pQueryRequest'), (1, 'pQueryResults'), (1, 'pCancelHandle'))



GetAdaptersInfoPrototype = WINFUNCTYPE(ULONG, PIP_ADAPTER_INFO, PULONG)
GetAdaptersInfoParams = ((1, 'AdapterInfo'), (1, 'SizePointer'))



GetPerAdapterInfoPrototype = WINFUNCTYPE(DWORD, ULONG, PIP_PER_ADAPTER_INFO, PULONG)
GetPerAdapterInfoParams = ((1, 'IfIndex'), (1, 'pPerAdapterInfo'), (1, 'pOutBufLen'))



CreateFileTransactedAPrototype = WINFUNCTYPE(HANDLE, LPCSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE, HANDLE, PUSHORT, PVOID)
CreateFileTransactedAParams = ((1, 'lpFileName'), (1, 'dwDesiredAccess'), (1, 'dwShareMode'), (1, 'lpSecurityAttributes'), (1, 'dwCreationDisposition'), (1, 'dwFlagsAndAttributes'), (1, 'hTemplateFile'), (1, 'hTransaction'), (1, 'pusMiniVersion'), (1, 'pExtendedParameter'))



CreateFileTransactedWPrototype = WINFUNCTYPE(HANDLE, LPWSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE, HANDLE, PUSHORT, PVOID)
CreateFileTransactedWParams = ((1, 'lpFileName'), (1, 'dwDesiredAccess'), (1, 'dwShareMode'), (1, 'lpSecurityAttributes'), (1, 'dwCreationDisposition'), (1, 'dwFlagsAndAttributes'), (1, 'hTemplateFile'), (1, 'hTransaction'), (1, 'pusMiniVersion'), (1, 'pExtendedParameter'))



CommitTransactionPrototype = WINFUNCTYPE(BOOL, HANDLE)
CommitTransactionParams = ((1, 'TransactionHandle'),)



CreateTransactionPrototype = WINFUNCTYPE(HANDLE, LPSECURITY_ATTRIBUTES, LPGUID, DWORD, DWORD, DWORD, DWORD, LPWSTR)
CreateTransactionParams = ((1, 'lpTransactionAttributes'), (1, 'UOW'), (1, 'CreateOptions'), (1, 'IsolationLevel'), (1, 'IsolationFlags'), (1, 'Timeout'), (1, 'Description'))



RollbackTransactionPrototype = WINFUNCTYPE(BOOL, HANDLE)
RollbackTransactionParams = ((1, 'TransactionHandle'),)



OpenTransactionPrototype = WINFUNCTYPE(HANDLE, DWORD, LPGUID)
OpenTransactionParams = ((1, 'dwDesiredAccess'), (1, 'TransactionId'))



NtOpenKeyPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES)
NtOpenKeyParams = ((1, 'KeyHandle'), (1, 'DesiredAccess'), (1, 'ObjectAttributes'))



NtCreateKeyPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, ULONG, PUNICODE_STRING, ULONG, PULONG)
NtCreateKeyParams = ((1, 'pKeyHandle'), (1, 'DesiredAccess'), (1, 'ObjectAttributes'), (1, 'TitleIndex'), (1, 'Class'), (1, 'CreateOptions'), (1, 'Disposition'))



NtSetValueKeyPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PUNICODE_STRING, ULONG, ULONG, PVOID, ULONG)
NtSetValueKeyParams = ((1, 'KeyHandle'), (1, 'ValueName'), (1, 'TitleIndex'), (1, 'Type'), (1, 'Data'), (1, 'DataSize'))



NtQueryValueKeyPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PUNICODE_STRING, KEY_VALUE_INFORMATION_CLASS, PVOID, ULONG, PULONG)
NtQueryValueKeyParams = ((1, 'KeyHandle'), (1, 'ValueName'), (1, 'KeyValueInformationClass'), (1, 'KeyValueInformation'), (1, 'Length'), (1, 'ResultLength'))



NtQueryKeyPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, KEY_INFORMATION_CLASS, PVOID, ULONG, PULONG)
NtQueryKeyParams = ((1, 'KeyHandle'), (1, 'KeyInformationClass'), (1, 'KeyInformation'), (1, 'Length'), (1, 'ResultLength'))



NtEnumerateValueKeyPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, ULONG, KEY_VALUE_INFORMATION_CLASS, PVOID, ULONG, PULONG)
NtEnumerateValueKeyParams = ((1, 'KeyHandle'), (1, 'Index'), (1, 'KeyValueInformationClass'), (1, 'KeyValueInformation'), (1, 'Length'), (1, 'ResultLength'))



NtDeleteValueKeyPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PUNICODE_STRING)
NtDeleteValueKeyParams = ((1, 'KeyHandle'), (1, 'ValueName'))



CreatePipePrototype = WINFUNCTYPE(BOOL, PHANDLE, PHANDLE, LPSECURITY_ATTRIBUTES, DWORD)
CreatePipeParams = ((1, 'hReadPipe'), (1, 'hWritePipe'), (1, 'lpPipeAttributes'), (1, 'nSize'))



CreateNamedPipeAPrototype = WINFUNCTYPE(HANDLE, LPCSTR, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, LPSECURITY_ATTRIBUTES)
CreateNamedPipeAParams = ((1, 'lpName'), (1, 'dwOpenMode'), (1, 'dwPipeMode'), (1, 'nMaxInstances'), (1, 'nOutBufferSize'), (1, 'nInBufferSize'), (1, 'nDefaultTimeOut'), (1, 'lpSecurityAttributes'))



CreateNamedPipeWPrototype = WINFUNCTYPE(HANDLE, LPWSTR, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, LPSECURITY_ATTRIBUTES)
CreateNamedPipeWParams = ((1, 'lpName'), (1, 'dwOpenMode'), (1, 'dwPipeMode'), (1, 'nMaxInstances'), (1, 'nOutBufferSize'), (1, 'nInBufferSize'), (1, 'nDefaultTimeOut'), (1, 'lpSecurityAttributes'))



ConnectNamedPipePrototype = WINFUNCTYPE(BOOL, HANDLE, LPOVERLAPPED)
ConnectNamedPipeParams = ((1, 'hNamedPipe'), (1, 'lpOverlapped'))



SetNamedPipeHandleStatePrototype = WINFUNCTYPE(BOOL, HANDLE, LPDWORD, LPDWORD, LPDWORD)
SetNamedPipeHandleStateParams = ((1, 'hNamedPipe'), (1, 'lpMode'), (1, 'lpMaxCollectionCount'), (1, 'lpCollectDataTimeout'))



PeekNamedPipePrototype = WINFUNCTYPE(BOOL, HANDLE, LPVOID, DWORD, LPDWORD, LPDWORD, LPDWORD)
PeekNamedPipeParams = ((1, 'hNamedPipe'), (1, 'lpBuffer'), (1, 'nBufferSize'), (1, 'lpBytesRead'), (1, 'lpTotalBytesAvail'), (1, 'lpBytesLeftThisMessage'))



CreateToolhelp32SnapshotPrototype = WINFUNCTYPE(HANDLE, DWORD, DWORD)
CreateToolhelp32SnapshotParams = ((1, 'dwFlags'), (1, 'th32ProcessID'))



Thread32FirstPrototype = WINFUNCTYPE(BOOL, HANDLE, LPTHREADENTRY32)
Thread32FirstParams = ((1, 'hSnapshot'), (1, 'lpte'))



Thread32NextPrototype = WINFUNCTYPE(BOOL, HANDLE, LPTHREADENTRY32)
Thread32NextParams = ((1, 'hSnapshot'), (1, 'lpte'))



Process32FirstPrototype = WINFUNCTYPE(BOOL, HANDLE, LPPROCESSENTRY32)
Process32FirstParams = ((1, 'hSnapshot'), (1, 'lppe'))



Process32NextPrototype = WINFUNCTYPE(BOOL, HANDLE, LPPROCESSENTRY32)
Process32NextParams = ((1, 'hSnapshot'), (1, 'lppe'))



Process32FirstWPrototype = WINFUNCTYPE(BOOL, HANDLE, LPPROCESSENTRY32W)
Process32FirstWParams = ((1, 'hSnapshot'), (1, 'lppe'))



Process32NextWPrototype = WINFUNCTYPE(BOOL, HANDLE, LPPROCESSENTRY32W)
Process32NextWParams = ((1, 'hSnapshot'), (1, 'lppe'))



GetProcAddressPrototype = WINFUNCTYPE(FARPROC, HMODULE, LPCSTR)
GetProcAddressParams = ((1, 'hModule'), (1, 'lpProcName'))



LoadLibraryAPrototype = WINFUNCTYPE(HMODULE, LPCSTR)
LoadLibraryAParams = ((1, 'lpFileName'),)



LoadLibraryWPrototype = WINFUNCTYPE(HMODULE, LPCWSTR)
LoadLibraryWParams = ((1, 'lpFileName'),)



LoadLibraryExAPrototype = WINFUNCTYPE(HMODULE, LPCSTR, HANDLE, DWORD)
LoadLibraryExAParams = ((1, 'lpLibFileName'), (1, 'hFile'), (1, 'dwFlags'))



LoadLibraryExWPrototype = WINFUNCTYPE(HMODULE, LPCWSTR, HANDLE, DWORD)
LoadLibraryExWParams = ((1, 'lpLibFileName'), (1, 'hFile'), (1, 'dwFlags'))



FreeLibraryPrototype = WINFUNCTYPE(BOOL, HMODULE)
FreeLibraryParams = ((1, 'hLibModule'),)



RegQueryValueExAPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCSTR, LPDWORD, LPDWORD, LPBYTE, LPDWORD)
RegQueryValueExAParams = ((1, 'hKey'), (1, 'lpValueName'), (1, 'lpReserved'), (1, 'lpType'), (1, 'lpData'), (1, 'lpcbData'))



RegQueryValueExWPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPWSTR, LPDWORD, LPDWORD, LPBYTE, LPDWORD)
RegQueryValueExWParams = ((1, 'hKey'), (1, 'lpValueName'), (1, 'lpReserved'), (1, 'lpType'), (1, 'lpData'), (1, 'lpcbData'))



RegOpenKeyExAPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCSTR, DWORD, REGSAM, PHKEY)
RegOpenKeyExAParams = ((1, 'hKey'), (1, 'lpSubKey'), (1, 'ulOptions'), (1, 'samDesired'), (1, 'phkResult'))



RegOpenKeyExWPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPWSTR, DWORD, REGSAM, PHKEY)
RegOpenKeyExWParams = ((1, 'hKey'), (1, 'lpSubKey'), (1, 'ulOptions'), (1, 'samDesired'), (1, 'phkResult'))



RegCreateKeyExAPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCSTR, DWORD, LPSTR, DWORD, REGSAM, LPSECURITY_ATTRIBUTES, PHKEY, LPDWORD)
RegCreateKeyExAParams = ((1, 'hKey'), (1, 'lpSubKey'), (1, 'Reserved'), (1, 'lpClass'), (1, 'dwOptions'), (1, 'samDesired'), (1, 'lpSecurityAttributes'), (1, 'phkResult'), (1, 'lpdwDisposition'))



RegCreateKeyExWPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCWSTR, DWORD, LPWSTR, DWORD, REGSAM, LPSECURITY_ATTRIBUTES, PHKEY, LPDWORD)
RegCreateKeyExWParams = ((1, 'hKey'), (1, 'lpSubKey'), (1, 'Reserved'), (1, 'lpClass'), (1, 'dwOptions'), (1, 'samDesired'), (1, 'lpSecurityAttributes'), (1, 'phkResult'), (1, 'lpdwDisposition'))



RegGetValueAPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCSTR, LPCSTR, DWORD, LPDWORD, PVOID, LPDWORD)
RegGetValueAParams = ((1, 'hkey'), (1, 'lpSubKey'), (1, 'lpValue'), (1, 'dwFlags'), (1, 'pdwType'), (1, 'pvData'), (1, 'pcbData'))



RegGetValueWPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPWSTR, LPWSTR, DWORD, LPDWORD, PVOID, LPDWORD)
RegGetValueWParams = ((1, 'hkey'), (1, 'lpSubKey'), (1, 'lpValue'), (1, 'dwFlags'), (1, 'pdwType'), (1, 'pvData'), (1, 'pcbData'))



RegCloseKeyPrototype = WINFUNCTYPE(LSTATUS, HKEY)
RegCloseKeyParams = ((1, 'hKey'),)



RegSetValueExWPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCWSTR, DWORD, DWORD, POINTER(BYTE), DWORD)
RegSetValueExWParams = ((1, 'hKey'), (1, 'lpValueName'), (1, 'Reserved'), (1, 'dwType'), (1, 'lpData'), (1, 'cbData'))



RegSetValueExAPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCSTR, DWORD, DWORD, POINTER(BYTE), DWORD)
RegSetValueExAParams = ((1, 'hKey'), (1, 'lpValueName'), (1, 'Reserved'), (1, 'dwType'), (1, 'lpData'), (1, 'cbData'))



RegSetKeyValueAPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCSTR, LPCSTR, DWORD, LPCVOID, DWORD)
RegSetKeyValueAParams = ((1, 'hKey'), (1, 'lpSubKey'), (1, 'lpValueName'), (1, 'dwType'), (1, 'lpData'), (1, 'cbData'))



RegSetKeyValueWPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCWSTR, LPCWSTR, DWORD, LPCVOID, DWORD)
RegSetKeyValueWParams = ((1, 'hKey'), (1, 'lpSubKey'), (1, 'lpValueName'), (1, 'dwType'), (1, 'lpData'), (1, 'cbData'))



RegEnumKeyExAPrototype = WINFUNCTYPE(LSTATUS, HKEY, DWORD, LPSTR, LPDWORD, LPDWORD, LPSTR, LPDWORD, PFILETIME)
RegEnumKeyExAParams = ((1, 'hKey'), (1, 'dwIndex'), (1, 'lpName'), (1, 'lpcchName'), (1, 'lpReserved'), (1, 'lpClass'), (1, 'lpcchClass'), (1, 'lpftLastWriteTime'))



RegEnumKeyExWPrototype = WINFUNCTYPE(LSTATUS, HKEY, DWORD, LPWSTR, LPDWORD, LPDWORD, LPWSTR, LPDWORD, PFILETIME)
RegEnumKeyExWParams = ((1, 'hKey'), (1, 'dwIndex'), (1, 'lpName'), (1, 'lpcchName'), (1, 'lpReserved'), (1, 'lpClass'), (1, 'lpcchClass'), (1, 'lpftLastWriteTime'))



RegGetKeySecurityPrototype = WINFUNCTYPE(LSTATUS, HKEY, SECURITY_INFORMATION, PSECURITY_DESCRIPTOR, LPDWORD)
RegGetKeySecurityParams = ((1, 'hKey'), (1, 'SecurityInformation'), (1, 'pSecurityDescriptor'), (1, 'lpcbSecurityDescriptor'))



RegQueryInfoKeyAPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPSTR, LPDWORD, LPDWORD, LPDWORD, LPDWORD, LPDWORD, LPDWORD, LPDWORD, LPDWORD, LPDWORD, PFILETIME)
RegQueryInfoKeyAParams = ((1, 'hKey'), (1, 'lpClass'), (1, 'lpcchClass'), (1, 'lpReserved'), (1, 'lpcSubKeys'), (1, 'lpcbMaxSubKeyLen'), (1, 'lpcbMaxClassLen'), (1, 'lpcValues'), (1, 'lpcbMaxValueNameLen'), (1, 'lpcbMaxValueLen'), (1, 'lpcbSecurityDescriptor'), (1, 'lpftLastWriteTime'))



RegQueryInfoKeyWPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPWSTR, LPDWORD, LPDWORD, LPDWORD, LPDWORD, LPDWORD, LPDWORD, LPDWORD, LPDWORD, LPDWORD, PFILETIME)
RegQueryInfoKeyWParams = ((1, 'hKey'), (1, 'lpClass'), (1, 'lpcchClass'), (1, 'lpReserved'), (1, 'lpcSubKeys'), (1, 'lpcbMaxSubKeyLen'), (1, 'lpcbMaxClassLen'), (1, 'lpcValues'), (1, 'lpcbMaxValueNameLen'), (1, 'lpcbMaxValueLen'), (1, 'lpcbSecurityDescriptor'), (1, 'lpftLastWriteTime'))



RegDeleteKeyValueWPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCWSTR, LPCWSTR)
RegDeleteKeyValueWParams = ((1, 'hKey'), (1, 'lpSubKey'), (1, 'lpValueName'))



RegDeleteKeyValueAPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCSTR, LPCSTR)
RegDeleteKeyValueAParams = ((1, 'hKey'), (1, 'lpSubKey'), (1, 'lpValueName'))



RegDeleteKeyExAPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCSTR, REGSAM, DWORD)
RegDeleteKeyExAParams = ((1, 'hKey'), (1, 'lpSubKey'), (1, 'samDesired'), (1, 'Reserved'))



RegDeleteKeyExWPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCWSTR, REGSAM, DWORD)
RegDeleteKeyExWParams = ((1, 'hKey'), (1, 'lpSubKey'), (1, 'samDesired'), (1, 'Reserved'))



RegDeleteValueAPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCSTR)
RegDeleteValueAParams = ((1, 'hKey'), (1, 'lpValueName'))



RegDeleteValueWPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCWSTR)
RegDeleteValueWParams = ((1, 'hKey'), (1, 'lpValueName'))



RegEnumValueAPrototype = WINFUNCTYPE(LSTATUS, HKEY, DWORD, LPSTR, LPDWORD, LPDWORD, LPDWORD, LPBYTE, LPDWORD)
RegEnumValueAParams = ((1, 'hKey'), (1, 'dwIndex'), (1, 'lpValueName'), (1, 'lpcchValueName'), (1, 'lpReserved'), (1, 'lpType'), (1, 'lpData'), (1, 'lpcbData'))



RegEnumValueWPrototype = WINFUNCTYPE(LSTATUS, HKEY, DWORD, LPWSTR, LPDWORD, LPDWORD, LPDWORD, LPBYTE, LPDWORD)
RegEnumValueWParams = ((1, 'hKey'), (1, 'dwIndex'), (1, 'lpValueName'), (1, 'lpcchValueName'), (1, 'lpReserved'), (1, 'lpType'), (1, 'lpData'), (1, 'lpcbData'))



RegDeleteTreeAPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCSTR)
RegDeleteTreeAParams = ((1, 'hKey'), (1, 'lpSubKey'))



RegDeleteTreeWPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCWSTR)
RegDeleteTreeWParams = ((1, 'hKey'), (1, 'lpSubKey'))



RegSaveKeyAPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCSTR, LPSECURITY_ATTRIBUTES)
RegSaveKeyAParams = ((1, 'hKey'), (1, 'lpFile'), (1, 'lpSecurityAttributes'))



RegSaveKeyWPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCWSTR, LPSECURITY_ATTRIBUTES)
RegSaveKeyWParams = ((1, 'hKey'), (1, 'lpFile'), (1, 'lpSecurityAttributes'))



RegSaveKeyExAPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCSTR, LPSECURITY_ATTRIBUTES, DWORD)
RegSaveKeyExAParams = ((1, 'hKey'), (1, 'lpFile'), (1, 'lpSecurityAttributes'), (1, 'Flags'))



RegSaveKeyExWPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCWSTR, LPSECURITY_ATTRIBUTES, DWORD)
RegSaveKeyExWParams = ((1, 'hKey'), (1, 'lpFile'), (1, 'lpSecurityAttributes'), (1, 'Flags'))



RegLoadKeyAPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCSTR, LPCSTR)
RegLoadKeyAParams = ((1, 'hKey'), (1, 'lpSubKey'), (1, 'lpFile'))



RegLoadKeyWPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCWSTR, LPCWSTR)
RegLoadKeyWParams = ((1, 'hKey'), (1, 'lpSubKey'), (1, 'lpFile'))



RegUnLoadKeyAPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCSTR)
RegUnLoadKeyAParams = ((1, 'hKey'), (1, 'lpSubKey'))



RegUnLoadKeyWPrototype = WINFUNCTYPE(LSTATUS, HKEY, LPCWSTR)
RegUnLoadKeyWParams = ((1, 'hKey'), (1, 'lpSubKey'))



IsValidSecurityDescriptorPrototype = WINFUNCTYPE(BOOL, PSECURITY_DESCRIPTOR)
IsValidSecurityDescriptorParams = ((1, 'pSecurityDescriptor'),)



ConvertStringSecurityDescriptorToSecurityDescriptorAPrototype = WINFUNCTYPE(BOOL, LPCSTR, DWORD, POINTER(PSECURITY_DESCRIPTOR), PULONG)
ConvertStringSecurityDescriptorToSecurityDescriptorAParams = ((1, 'StringSecurityDescriptor'), (1, 'StringSDRevision'), (1, 'SecurityDescriptor'), (1, 'SecurityDescriptorSize'))



ConvertStringSecurityDescriptorToSecurityDescriptorWPrototype = WINFUNCTYPE(BOOL, LPWSTR, DWORD, POINTER(PSECURITY_DESCRIPTOR), PULONG)
ConvertStringSecurityDescriptorToSecurityDescriptorWParams = ((1, 'StringSecurityDescriptor'), (1, 'StringSDRevision'), (1, 'SecurityDescriptor'), (1, 'SecurityDescriptorSize'))



ConvertSecurityDescriptorToStringSecurityDescriptorAPrototype = WINFUNCTYPE(BOOL, PSECURITY_DESCRIPTOR, DWORD, DWORD, POINTER(LPCSTR), PULONG)
ConvertSecurityDescriptorToStringSecurityDescriptorAParams = ((1, 'SecurityDescriptor'), (1, 'RequestedStringSDRevision'), (1, 'SecurityInformation'), (1, 'StringSecurityDescriptor'), (1, 'StringSecurityDescriptorLen'))



ConvertSecurityDescriptorToStringSecurityDescriptorWPrototype = WINFUNCTYPE(BOOL, PSECURITY_DESCRIPTOR, DWORD, DWORD, POINTER(LPWSTR), PULONG)
ConvertSecurityDescriptorToStringSecurityDescriptorWParams = ((1, 'SecurityDescriptor'), (1, 'RequestedStringSDRevision'), (1, 'SecurityInformation'), (1, 'StringSecurityDescriptor'), (1, 'StringSecurityDescriptorLen'))



GetSecurityDescriptorControlPrototype = WINFUNCTYPE(BOOL, PSECURITY_DESCRIPTOR, PSECURITY_DESCRIPTOR_CONTROL, LPDWORD)
GetSecurityDescriptorControlParams = ((1, 'pSecurityDescriptor'), (1, 'pControl'), (1, 'lpdwRevision'))



GetSecurityDescriptorDaclPrototype = WINFUNCTYPE(BOOL, PSECURITY_DESCRIPTOR, LPBOOL, POINTER(PACL), LPBOOL)
GetSecurityDescriptorDaclParams = ((1, 'pSecurityDescriptor'), (1, 'lpbDaclPresent'), (1, 'pDacl'), (1, 'lpbDaclDefaulted'))



GetSecurityDescriptorGroupPrototype = WINFUNCTYPE(BOOL, PSECURITY_DESCRIPTOR, POINTER(PSID), LPBOOL)
GetSecurityDescriptorGroupParams = ((1, 'pSecurityDescriptor'), (1, 'pGroup'), (1, 'lpbGroupDefaulted'))



GetSecurityDescriptorLengthPrototype = WINFUNCTYPE(DWORD, PSECURITY_DESCRIPTOR)
GetSecurityDescriptorLengthParams = ((1, 'pSecurityDescriptor'),)



GetSecurityDescriptorOwnerPrototype = WINFUNCTYPE(BOOL, PSECURITY_DESCRIPTOR, POINTER(PSID), LPBOOL)
GetSecurityDescriptorOwnerParams = ((1, 'pSecurityDescriptor'), (1, 'pOwner'), (1, 'lpbOwnerDefaulted'))



SetSecurityDescriptorOwnerPrototype = WINFUNCTYPE(BOOL, PSECURITY_DESCRIPTOR, PSID, BOOL)
SetSecurityDescriptorOwnerParams = ((1, 'pSecurityDescriptor'), (1, 'pOwner'), (1, 'bOwnerDefaulted'))



GetSecurityDescriptorRMControlPrototype = WINFUNCTYPE(DWORD, PSECURITY_DESCRIPTOR, PUCHAR)
GetSecurityDescriptorRMControlParams = ((1, 'SecurityDescriptor'), (1, 'RMControl'))



GetSecurityDescriptorSaclPrototype = WINFUNCTYPE(BOOL, PSECURITY_DESCRIPTOR, LPBOOL, POINTER(PACL), LPBOOL)
GetSecurityDescriptorSaclParams = ((1, 'pSecurityDescriptor'), (1, 'lpbSaclPresent'), (1, 'pSacl'), (1, 'lpbSaclDefaulted'))



GetLengthSidPrototype = WINFUNCTYPE(DWORD, PSID)
GetLengthSidParams = ((1, 'pSid'),)



EqualSidPrototype = WINFUNCTYPE(BOOL, PSID, PSID)
EqualSidParams = ((1, 'pSid1'), (1, 'pSid2'))



CopySidPrototype = WINFUNCTYPE(BOOL, DWORD, PSID, PSID)
CopySidParams = ((1, 'nDestinationSidLength'), (1, 'pDestinationSid'), (1, 'pSourceSid'))



GetSidIdentifierAuthorityPrototype = WINFUNCTYPE(PSID_IDENTIFIER_AUTHORITY, PSID)
GetSidIdentifierAuthorityParams = ((1, 'pSid'),)



GetSidLengthRequiredPrototype = WINFUNCTYPE(DWORD, UCHAR)
GetSidLengthRequiredParams = ((1, 'nSubAuthorityCount'),)



GetSidSubAuthorityPrototype = WINFUNCTYPE(PDWORD, PSID, DWORD)
GetSidSubAuthorityParams = ((1, 'pSid'), (1, 'nSubAuthority'))



GetSidSubAuthorityCountPrototype = WINFUNCTYPE(LPBYTE, PSID)
GetSidSubAuthorityCountParams = ((1, 'pSid'),)



FreeSidPrototype = WINFUNCTYPE(PVOID, PSID)
FreeSidParams = ((1, 'pSid'),)



GetAcePrototype = WINFUNCTYPE(BOOL, PACL, DWORD, POINTER(LPVOID))
GetAceParams = ((1, 'pAcl'), (1, 'dwAceIndex'), (1, 'pAce'))



GetAclInformationPrototype = WINFUNCTYPE(BOOL, PACL, LPVOID, DWORD, ACL_INFORMATION_CLASS)
GetAclInformationParams = ((1, 'pAcl'), (1, 'pAclInformation'), (1, 'nAclInformationLength'), (1, 'dwAclInformationClass'))



MapGenericMaskPrototype = WINFUNCTYPE(PVOID, PDWORD, PGENERIC_MAPPING)
MapGenericMaskParams = ((1, 'AccessMask'), (1, 'GenericMapping'))



AccessCheckPrototype = WINFUNCTYPE(BOOL, PSECURITY_DESCRIPTOR, HANDLE, DWORD, PGENERIC_MAPPING, PPRIVILEGE_SET, LPDWORD, LPDWORD, LPBOOL)
AccessCheckParams = ((1, 'pSecurityDescriptor'), (1, 'ClientToken'), (1, 'DesiredAccess'), (1, 'GenericMapping'), (1, 'PrivilegeSet'), (1, 'PrivilegeSetLength'), (1, 'GrantedAccess'), (1, 'AccessStatus'))



GetNamedSecurityInfoAPrototype = WINFUNCTYPE(DWORD, LPCSTR, SE_OBJECT_TYPE, SECURITY_INFORMATION, POINTER(PSID), POINTER(PSID), POINTER(PACL), POINTER(PACL), POINTER(PSECURITY_DESCRIPTOR))
GetNamedSecurityInfoAParams = ((1, 'pObjectName'), (1, 'ObjectType'), (1, 'SecurityInfo'), (1, 'ppsidOwner'), (1, 'ppsidGroup'), (1, 'ppDacl'), (1, 'ppSacl'), (1, 'ppSecurityDescriptor'))



GetNamedSecurityInfoWPrototype = WINFUNCTYPE(DWORD, LPWSTR, SE_OBJECT_TYPE, SECURITY_INFORMATION, POINTER(PSID), POINTER(PSID), POINTER(PACL), POINTER(PACL), POINTER(PSECURITY_DESCRIPTOR))
GetNamedSecurityInfoWParams = ((1, 'pObjectName'), (1, 'ObjectType'), (1, 'SecurityInfo'), (1, 'ppsidOwner'), (1, 'ppsidGroup'), (1, 'ppDacl'), (1, 'ppSacl'), (1, 'ppSecurityDescriptor'))



GetSecurityInfoPrototype = WINFUNCTYPE(DWORD, HANDLE, SE_OBJECT_TYPE, SECURITY_INFORMATION, POINTER(PSID), POINTER(PSID), POINTER(PACL), POINTER(PACL), POINTER(PSECURITY_DESCRIPTOR))
GetSecurityInfoParams = ((1, 'handle'), (1, 'ObjectType'), (1, 'SecurityInfo'), (1, 'ppsidOwner'), (1, 'ppsidGroup'), (1, 'ppDacl'), (1, 'ppSacl'), (1, 'ppSecurityDescriptor'))



SetSecurityInfoPrototype = WINFUNCTYPE(DWORD, HANDLE, SE_OBJECT_TYPE, SECURITY_INFORMATION, PSID, PSID, PACL, PACL)
SetSecurityInfoParams = ((1, 'handle'), (1, 'ObjectType'), (1, 'SecurityInfo'), (1, 'psidOwner'), (1, 'psidGroup'), (1, 'pDacl'), (1, 'pSacl'))



SetNamedSecurityInfoAPrototype = WINFUNCTYPE(DWORD, LPSTR, SE_OBJECT_TYPE, SECURITY_INFORMATION, PSID, PSID, PACL, PACL)
SetNamedSecurityInfoAParams = ((1, 'pObjectName'), (1, 'ObjectType'), (1, 'SecurityInfo'), (1, 'psidOwner'), (1, 'psidGroup'), (1, 'pDacl'), (1, 'pSacl'))



SetNamedSecurityInfoWPrototype = WINFUNCTYPE(DWORD, LPWSTR, SE_OBJECT_TYPE, SECURITY_INFORMATION, PSID, PSID, PACL, PACL)
SetNamedSecurityInfoWParams = ((1, 'pObjectName'), (1, 'ObjectType'), (1, 'SecurityInfo'), (1, 'psidOwner'), (1, 'psidGroup'), (1, 'pDacl'), (1, 'pSacl'))



GetStringConditionFromBinaryPrototype = WINFUNCTYPE(DWORD, POINTER(BYTE), DWORD, DWORD, POINTER(LPWSTR))
GetStringConditionFromBinaryParams = ((1, 'BinaryAceCondition'), (1, 'BinaryAceConditionSize'), (1, 'Reserved1'), (1, 'StringAceCondition'))



AddAccessAllowedAcePrototype = WINFUNCTYPE(BOOL, PACL, DWORD, DWORD, PSID)
AddAccessAllowedAceParams = ((1, 'pAcl'), (1, 'dwAceRevision'), (1, 'AccessMask'), (1, 'pSid'))



SetSecurityDescriptorDaclPrototype = WINFUNCTYPE(BOOL, PSECURITY_DESCRIPTOR, BOOL, PACL, BOOL)
SetSecurityDescriptorDaclParams = ((1, 'pSecurityDescriptor'), (1, 'bDaclPresent'), (1, 'pDacl'), (1, 'bDaclDefaulted'))



InitializeAclPrototype = WINFUNCTYPE(BOOL, PACL, DWORD, DWORD)
InitializeAclParams = ((1, 'pAcl'), (1, 'nAclLength'), (1, 'dwAclRevision'))



InitializeSecurityDescriptorPrototype = WINFUNCTYPE(BOOL, PSECURITY_DESCRIPTOR, DWORD)
InitializeSecurityDescriptorParams = ((1, 'pSecurityDescriptor'), (1, 'dwRevision'))



SetAclInformationPrototype = WINFUNCTYPE(BOOL, PACL, LPVOID, DWORD, ACL_INFORMATION_CLASS)
SetAclInformationParams = ((1, 'pAcl'), (1, 'pAclInformation'), (1, 'nAclInformationLength'), (1, 'dwAclInformationClass'))



AddAccessAllowedAceExPrototype = WINFUNCTYPE(BOOL, PACL, DWORD, DWORD, DWORD, PSID)
AddAccessAllowedAceExParams = ((1, 'pAcl'), (1, 'dwAceRevision'), (1, 'AceFlags'), (1, 'AccessMask'), (1, 'pSid'))



AddAccessDeniedAcePrototype = WINFUNCTYPE(BOOL, PACL, DWORD, DWORD, PSID)
AddAccessDeniedAceParams = ((1, 'pAcl'), (1, 'dwAceRevision'), (1, 'AccessMask'), (1, 'pSid'))



AddAccessDeniedAceExPrototype = WINFUNCTYPE(BOOL, PACL, DWORD, DWORD, DWORD, PSID)
AddAccessDeniedAceExParams = ((1, 'pAcl'), (1, 'dwAceRevision'), (1, 'AceFlags'), (1, 'AccessMask'), (1, 'pSid'))



BuildSecurityDescriptorWPrototype = WINFUNCTYPE(DWORD, PTRUSTEE_W, PTRUSTEE_W, ULONG, PEXPLICIT_ACCESS_W, ULONG, PEXPLICIT_ACCESS_W, PSECURITY_DESCRIPTOR, PULONG, POINTER(PSECURITY_DESCRIPTOR))
BuildSecurityDescriptorWParams = ((1, 'pOwner'), (1, 'pGroup'), (1, 'cCountOfAccessEntries'), (1, 'pListOfAccessEntries'), (1, 'cCountOfAuditEntries'), (1, 'pListOfAuditEntries'), (1, 'pOldSD'), (1, 'pSizeNewSD'), (1, 'pNewSD'))



MakeAbsoluteSDPrototype = WINFUNCTYPE(BOOL, PSECURITY_DESCRIPTOR, PSECURITY_DESCRIPTOR, LPDWORD, PACL, LPDWORD, PACL, LPDWORD, PSID, LPDWORD, PSID, LPDWORD)
MakeAbsoluteSDParams = ((1, 'pSelfRelativeSecurityDescriptor'), (1, 'pAbsoluteSecurityDescriptor'), (1, 'lpdwAbsoluteSecurityDescriptorSize'), (1, 'pDacl'), (1, 'lpdwDaclSize'), (1, 'pSacl'), (1, 'lpdwSaclSize'), (1, 'pOwner'), (1, 'lpdwOwnerSize'), (1, 'pPrimaryGroup'), (1, 'lpdwPrimaryGroupSize'))



MakeSelfRelativeSDPrototype = WINFUNCTYPE(BOOL, PSECURITY_DESCRIPTOR, PSECURITY_DESCRIPTOR, LPDWORD)
MakeSelfRelativeSDParams = ((1, 'pAbsoluteSecurityDescriptor'), (1, 'pSelfRelativeSecurityDescriptor'), (1, 'lpdwBufferLength'))



InitializeSecurityDescriptorPrototype = WINFUNCTYPE(BOOL, PSECURITY_DESCRIPTOR, DWORD)
InitializeSecurityDescriptorParams = ((1, 'pSecurityDescriptor'), (1, 'dwRevision'))



OpenSCManagerAPrototype = WINFUNCTYPE(SC_HANDLE, LPCSTR, LPCSTR, DWORD)
OpenSCManagerAParams = ((1, 'lpMachineName'), (1, 'lpDatabaseName'), (1, 'dwDesiredAccess'))



OpenSCManagerWPrototype = WINFUNCTYPE(SC_HANDLE, LPCWSTR, LPCWSTR, DWORD)
OpenSCManagerWParams = ((1, 'lpMachineName'), (1, 'lpDatabaseName'), (1, 'dwDesiredAccess'))



CloseServiceHandlePrototype = WINFUNCTYPE(BOOL, SC_HANDLE)
CloseServiceHandleParams = ((1, 'hSCObject'),)



EnumServicesStatusExAPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, SC_ENUM_TYPE, DWORD, DWORD, LPBYTE, DWORD, LPDWORD, LPDWORD, LPDWORD, LPCSTR)
EnumServicesStatusExAParams = ((1, 'hSCManager'), (1, 'InfoLevel'), (1, 'dwServiceType'), (1, 'dwServiceState'), (1, 'lpServices'), (1, 'cbBufSize'), (1, 'pcbBytesNeeded'), (1, 'lpServicesReturned'), (1, 'lpResumeHandle'), (1, 'pszGroupName'))



EnumServicesStatusExWPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, SC_ENUM_TYPE, DWORD, DWORD, LPBYTE, DWORD, LPDWORD, LPDWORD, LPDWORD, LPCWSTR)
EnumServicesStatusExWParams = ((1, 'hSCManager'), (1, 'InfoLevel'), (1, 'dwServiceType'), (1, 'dwServiceState'), (1, 'lpServices'), (1, 'cbBufSize'), (1, 'pcbBytesNeeded'), (1, 'lpServicesReturned'), (1, 'lpResumeHandle'), (1, 'pszGroupName'))



StartServiceAPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, DWORD, POINTER(LPCSTR))
StartServiceAParams = ((1, 'hService'), (1, 'dwNumServiceArgs'), (1, 'lpServiceArgVectors'))



StartServiceWPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, DWORD, POINTER(LPCWSTR))
StartServiceWParams = ((1, 'hService'), (1, 'dwNumServiceArgs'), (1, 'lpServiceArgVectors'))



OpenServiceAPrototype = WINFUNCTYPE(SC_HANDLE, SC_HANDLE, LPCSTR, DWORD)
OpenServiceAParams = ((1, 'hSCManager'), (1, 'lpServiceName'), (1, 'dwDesiredAccess'))



OpenServiceWPrototype = WINFUNCTYPE(SC_HANDLE, SC_HANDLE, LPCWSTR, DWORD)
OpenServiceWParams = ((1, 'hSCManager'), (1, 'lpServiceName'), (1, 'dwDesiredAccess'))



ControlServicePrototype = WINFUNCTYPE(BOOL, SC_HANDLE, DWORD, LPSERVICE_STATUS)
ControlServiceParams = ((1, 'hService'), (1, 'dwControl'), (1, 'lpServiceStatus'))



QueryServiceStatusPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, LPSERVICE_STATUS)
QueryServiceStatusParams = ((1, 'hService'), (1, 'lpServiceStatus'))



QueryServiceStatusExPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, SC_STATUS_TYPE, LPBYTE, DWORD, LPDWORD)
QueryServiceStatusExParams = ((1, 'hService'), (1, 'InfoLevel'), (1, 'lpBuffer'), (1, 'cbBufSize'), (1, 'pcbBytesNeeded'))



ChangeServiceConfig2APrototype = WINFUNCTYPE(BOOL, SC_HANDLE, DWORD, LPVOID)
ChangeServiceConfig2AParams = ((1, 'hService'), (1, 'dwInfoLevel'), (1, 'lpInfo'))



ChangeServiceConfig2WPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, DWORD, LPVOID)
ChangeServiceConfig2WParams = ((1, 'hService'), (1, 'dwInfoLevel'), (1, 'lpInfo'))



ChangeServiceConfigAPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, DWORD, DWORD, DWORD, LPCSTR, LPCSTR, LPDWORD, LPCSTR, LPCSTR, LPCSTR, LPCSTR)
ChangeServiceConfigAParams = ((1, 'hService'), (1, 'dwServiceType'), (1, 'dwStartType'), (1, 'dwErrorControl'), (1, 'lpBinaryPathName'), (1, 'lpLoadOrderGroup'), (1, 'lpdwTagId'), (1, 'lpDependencies'), (1, 'lpServiceStartName'), (1, 'lpPassword'), (1, 'lpDisplayName'))



ChangeServiceConfigWPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, DWORD, DWORD, DWORD, LPCWSTR, LPCWSTR, LPDWORD, LPCWSTR, LPCWSTR, LPCWSTR, LPCWSTR)
ChangeServiceConfigWParams = ((1, 'hService'), (1, 'dwServiceType'), (1, 'dwStartType'), (1, 'dwErrorControl'), (1, 'lpBinaryPathName'), (1, 'lpLoadOrderGroup'), (1, 'lpdwTagId'), (1, 'lpDependencies'), (1, 'lpServiceStartName'), (1, 'lpPassword'), (1, 'lpDisplayName'))



QueryServiceConfig2APrototype = WINFUNCTYPE(BOOL, SC_HANDLE, DWORD, LPBYTE, DWORD, LPDWORD)
QueryServiceConfig2AParams = ((1, 'hService'), (1, 'dwInfoLevel'), (1, 'lpBuffer'), (1, 'cbBufSize'), (1, 'pcbBytesNeeded'))



QueryServiceConfig2WPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, DWORD, LPBYTE, DWORD, LPDWORD)
QueryServiceConfig2WParams = ((1, 'hService'), (1, 'dwInfoLevel'), (1, 'lpBuffer'), (1, 'cbBufSize'), (1, 'pcbBytesNeeded'))



QueryServiceConfigAPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, LPQUERY_SERVICE_CONFIGA, DWORD, LPDWORD)
QueryServiceConfigAParams = ((1, 'hService'), (1, 'lpServiceConfig'), (1, 'cbBufSize'), (1, 'pcbBytesNeeded'))



QueryServiceConfigWPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, LPQUERY_SERVICE_CONFIGW, DWORD, LPDWORD)
QueryServiceConfigWParams = ((1, 'hService'), (1, 'lpServiceConfig'), (1, 'cbBufSize'), (1, 'pcbBytesNeeded'))



QueryServiceDynamicInformationPrototype = WINFUNCTYPE(BOOL, SERVICE_STATUS_HANDLE, DWORD, POINTER(PVOID))
QueryServiceDynamicInformationParams = ((1, 'hServiceStatus'), (1, 'dwInfoLevel'), (1, 'ppDynamicInfo'))



GetServiceDisplayNameAPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, LPCSTR, LPSTR, LPDWORD)
GetServiceDisplayNameAParams = ((1, 'hSCManager'), (1, 'lpServiceName'), (1, 'lpDisplayName'), (1, 'lpcchBuffer'))



GetServiceDisplayNameWPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, LPCWSTR, LPWSTR, LPDWORD)
GetServiceDisplayNameWParams = ((1, 'hSCManager'), (1, 'lpServiceName'), (1, 'lpDisplayName'), (1, 'lpcchBuffer'))



GetServiceKeyNameAPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, LPCSTR, LPSTR, LPDWORD)
GetServiceKeyNameAParams = ((1, 'hSCManager'), (1, 'lpDisplayName'), (1, 'lpServiceName'), (1, 'lpcchBuffer'))



GetServiceKeyNameWPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, LPCWSTR, LPWSTR, LPDWORD)
GetServiceKeyNameWParams = ((1, 'hSCManager'), (1, 'lpDisplayName'), (1, 'lpServiceName'), (1, 'lpcchBuffer'))



EnumDependentServicesAPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, DWORD, LPENUM_SERVICE_STATUSA, DWORD, LPDWORD, LPDWORD)
EnumDependentServicesAParams = ((1, 'hService'), (1, 'dwServiceState'), (1, 'lpServices'), (1, 'cbBufSize'), (1, 'pcbBytesNeeded'), (1, 'lpServicesReturned'))



EnumDependentServicesWPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, DWORD, LPENUM_SERVICE_STATUSW, DWORD, LPDWORD, LPDWORD)
EnumDependentServicesWParams = ((1, 'hService'), (1, 'dwServiceState'), (1, 'lpServices'), (1, 'cbBufSize'), (1, 'pcbBytesNeeded'), (1, 'lpServicesReturned'))



ControlServicePrototype = WINFUNCTYPE(BOOL, SC_HANDLE, DWORD, LPSERVICE_STATUS)
ControlServiceParams = ((1, 'hService'), (1, 'dwControl'), (1, 'lpServiceStatus'))



ControlServiceExAPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, DWORD, DWORD, PVOID)
ControlServiceExAParams = ((1, 'hService'), (1, 'dwControl'), (1, 'dwInfoLevel'), (1, 'pControlParams'))



ControlServiceExWPrototype = WINFUNCTYPE(BOOL, SC_HANDLE, DWORD, DWORD, PVOID)
ControlServiceExWParams = ((1, 'hService'), (1, 'dwControl'), (1, 'dwInfoLevel'), (1, 'pControlParams'))



CreateServiceAPrototype = WINFUNCTYPE(SC_HANDLE, SC_HANDLE, LPCSTR, LPCSTR, DWORD, DWORD, DWORD, DWORD, LPCSTR, LPCSTR, LPDWORD, LPCSTR, LPCSTR, LPCSTR)
CreateServiceAParams = ((1, 'hSCManager'), (1, 'lpServiceName'), (1, 'lpDisplayName'), (1, 'dwDesiredAccess'), (1, 'dwServiceType'), (1, 'dwStartType'), (1, 'dwErrorControl'), (1, 'lpBinaryPathName'), (1, 'lpLoadOrderGroup'), (1, 'lpdwTagId'), (1, 'lpDependencies'), (1, 'lpServiceStartName'), (1, 'lpPassword'))



CreateServiceWPrototype = WINFUNCTYPE(SC_HANDLE, SC_HANDLE, LPCWSTR, LPCWSTR, DWORD, DWORD, DWORD, DWORD, LPCWSTR, LPCWSTR, LPDWORD, LPCWSTR, LPCWSTR, LPCWSTR)
CreateServiceWParams = ((1, 'hSCManager'), (1, 'lpServiceName'), (1, 'lpDisplayName'), (1, 'dwDesiredAccess'), (1, 'dwServiceType'), (1, 'dwStartType'), (1, 'dwErrorControl'), (1, 'lpBinaryPathName'), (1, 'lpLoadOrderGroup'), (1, 'lpdwTagId'), (1, 'lpDependencies'), (1, 'lpServiceStartName'), (1, 'lpPassword'))



DeleteServicePrototype = WINFUNCTYPE(BOOL, SC_HANDLE)
DeleteServiceParams = ((1, 'hService'),)



StartServiceCtrlDispatcherAPrototype = WINFUNCTYPE(BOOL, POINTER(SERVICE_TABLE_ENTRYA))
StartServiceCtrlDispatcherAParams = ((1, 'lpServiceStartTable'),)



StartServiceCtrlDispatcherWPrototype = WINFUNCTYPE(BOOL, POINTER(SERVICE_TABLE_ENTRYW))
StartServiceCtrlDispatcherWParams = ((1, 'lpServiceStartTable'),)



SetupDiClassNameFromGuidAPrototype = WINFUNCTYPE(BOOL, POINTER(GUID), PSTR, DWORD, PDWORD)
SetupDiClassNameFromGuidAParams = ((1, 'ClassGuid'), (1, 'ClassName'), (1, 'ClassNameSize'), (1, 'RequiredSize'))



SetupDiClassNameFromGuidWPrototype = WINFUNCTYPE(BOOL, POINTER(GUID), PWSTR, DWORD, PDWORD)
SetupDiClassNameFromGuidWParams = ((1, 'ClassGuid'), (1, 'ClassName'), (1, 'ClassNameSize'), (1, 'RequiredSize'))



SetupDiClassNameFromGuidExAPrototype = WINFUNCTYPE(BOOL, POINTER(GUID), PSTR, DWORD, PDWORD, PCSTR, PVOID)
SetupDiClassNameFromGuidExAParams = ((1, 'ClassGuid'), (1, 'ClassName'), (1, 'ClassNameSize'), (1, 'RequiredSize'), (1, 'MachineName'), (1, 'Reserved'))



SetupDiClassNameFromGuidExWPrototype = WINFUNCTYPE(BOOL, POINTER(GUID), PWSTR, DWORD, PDWORD, PCWSTR, PVOID)
SetupDiClassNameFromGuidExWParams = ((1, 'ClassGuid'), (1, 'ClassName'), (1, 'ClassNameSize'), (1, 'RequiredSize'), (1, 'MachineName'), (1, 'Reserved'))



SetupDiGetClassDevsAPrototype = WINFUNCTYPE(HDEVINFO, POINTER(GUID), PCSTR, HWND, DWORD)
SetupDiGetClassDevsAParams = ((1, 'ClassGuid'), (1, 'Enumerator'), (1, 'hwndParent'), (1, 'Flags'))



SetupDiGetClassDevsWPrototype = WINFUNCTYPE(HDEVINFO, POINTER(GUID), PCWSTR, HWND, DWORD)
SetupDiGetClassDevsWParams = ((1, 'ClassGuid'), (1, 'Enumerator'), (1, 'hwndParent'), (1, 'Flags'))



SetupDiDeleteDeviceInfoPrototype = WINFUNCTYPE(BOOL, HDEVINFO, PSP_DEVINFO_DATA)
SetupDiDeleteDeviceInfoParams = ((1, 'DeviceInfoSet'), (1, 'DeviceInfoData'))



SetupDiEnumDeviceInfoPrototype = WINFUNCTYPE(BOOL, HDEVINFO, DWORD, PSP_DEVINFO_DATA)
SetupDiEnumDeviceInfoParams = ((1, 'DeviceInfoSet'), (1, 'MemberIndex'), (1, 'DeviceInfoData'))



SetupDiDestroyDeviceInfoListPrototype = WINFUNCTYPE(BOOL, HDEVINFO)
SetupDiDestroyDeviceInfoListParams = ((1, 'DeviceInfoSet'),)



SetupDiEnumDeviceInterfacesPrototype = WINFUNCTYPE(BOOL, HDEVINFO, PSP_DEVINFO_DATA, POINTER(GUID), DWORD, PSP_DEVICE_INTERFACE_DATA)
SetupDiEnumDeviceInterfacesParams = ((1, 'DeviceInfoSet'), (1, 'DeviceInfoData'), (1, 'InterfaceClassGuid'), (1, 'MemberIndex'), (1, 'DeviceInterfaceData'))



SetupDiGetDeviceRegistryPropertyAPrototype = WINFUNCTYPE(BOOL, HDEVINFO, PSP_DEVINFO_DATA, DWORD, PDWORD, PBYTE, DWORD, PDWORD)
SetupDiGetDeviceRegistryPropertyAParams = ((1, 'DeviceInfoSet'), (1, 'DeviceInfoData'), (1, 'Property'), (1, 'PropertyRegDataType'), (1, 'PropertyBuffer'), (1, 'PropertyBufferSize'), (1, 'RequiredSize'))



SetupDiGetDeviceRegistryPropertyWPrototype = WINFUNCTYPE(BOOL, HDEVINFO, PSP_DEVINFO_DATA, DWORD, PDWORD, PBYTE, DWORD, PDWORD)
SetupDiGetDeviceRegistryPropertyWParams = ((1, 'DeviceInfoSet'), (1, 'DeviceInfoData'), (1, 'Property'), (1, 'PropertyRegDataType'), (1, 'PropertyBuffer'), (1, 'PropertyBufferSize'), (1, 'RequiredSize'))



ShellExecuteAPrototype = WINFUNCTYPE(HINSTANCE, HWND, LPCSTR, LPCSTR, LPCSTR, LPCSTR, INT)
ShellExecuteAParams = ((1, 'hwnd'), (1, 'lpOperation'), (1, 'lpFile'), (1, 'lpParameters'), (1, 'lpDirectory'), (1, 'nShowCmd'))



ShellExecuteWPrototype = WINFUNCTYPE(HINSTANCE, HWND, LPWSTR, LPWSTR, LPWSTR, LPWSTR, INT)
ShellExecuteWParams = ((1, 'hwnd'), (1, 'lpOperation'), (1, 'lpFile'), (1, 'lpParameters'), (1, 'lpDirectory'), (1, 'nShowCmd'))



SHGetPathFromIDListAPrototype = WINFUNCTYPE(BOOL, PCIDLIST_ABSOLUTE, LPCSTR)
SHGetPathFromIDListAParams = ((1, 'pidl'), (1, 'pszPath'))



SHGetPathFromIDListWPrototype = WINFUNCTYPE(BOOL, PCIDLIST_ABSOLUTE, LPWSTR)
SHGetPathFromIDListWParams = ((1, 'pidl'), (1, 'pszPath'))



SHFileOperationAPrototype = WINFUNCTYPE(INT, LPSHFILEOPSTRUCTA)
SHFileOperationAParams = ((1, 'lpFileOp'),)



StrStrIWPrototype = WINFUNCTYPE(PWSTR, PWSTR, PWSTR)
StrStrIWParams = ((1, 'pszFirst'), (1, 'pszSrch'))



StrStrIAPrototype = WINFUNCTYPE(PCSTR, PCSTR, PCSTR)
StrStrIAParams = ((1, 'pszFirst'), (1, 'pszSrch'))



IsOSPrototype = WINFUNCTYPE(BOOL, DWORD)
IsOSParams = ((1, 'dwOS'),)



SymLoadModuleExAPrototype = WINFUNCTYPE(DWORD64, HANDLE, HANDLE, PCSTR, PCSTR, DWORD64, DWORD, PMODLOAD_DATA, DWORD)
SymLoadModuleExAParams = ((1, 'hProcess'), (1, 'hFile'), (1, 'ImageName'), (1, 'ModuleName'), (1, 'BaseOfDll'), (1, 'DllSize'), (1, 'Data'), (1, 'Flags'))



SymLoadModuleExWPrototype = WINFUNCTYPE(DWORD64, HANDLE, HANDLE, PCWSTR, PCWSTR, DWORD64, DWORD, PMODLOAD_DATA, DWORD)
SymLoadModuleExWParams = ((1, 'hProcess'), (1, 'hFile'), (1, 'ImageName'), (1, 'ModuleName'), (1, 'BaseOfDll'), (1, 'DllSize'), (1, 'Data'), (1, 'Flags'))



SymFromAddrPrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD64, PDWORD64, PSYMBOL_INFO)
SymFromAddrParams = ((1, 'hProcess'), (1, 'Address'), (1, 'Displacement'), (1, 'Symbol'))



SymGetModuleInfo64Prototype = WINFUNCTYPE(BOOL, HANDLE, DWORD64, PIMAGEHLP_MODULE64)
SymGetModuleInfo64Params = ((1, 'hProcess'), (1, 'dwAddr'), (1, 'ModuleInfo'))



SymGetModuleInfoW64Prototype = WINFUNCTYPE(BOOL, HANDLE, DWORD64, PIMAGEHLP_MODULEW64)
SymGetModuleInfoW64Params = ((1, 'hProcess'), (1, 'qwAddr'), (1, 'ModuleInfo'))



SymInitializePrototype = WINFUNCTYPE(BOOL, HANDLE, LPCSTR, BOOL)
SymInitializeParams = ((1, 'hProcess'), (1, 'UserSearchPath'), (1, 'fInvadeProcess'))



SymFromNamePrototype = WINFUNCTYPE(BOOL, HANDLE, LPCSTR, PSYMBOL_INFO)
SymFromNameParams = ((1, 'hProcess'), (1, 'Name'), (1, 'Symbol'))



SymFromNameWPrototype = WINFUNCTYPE(BOOL, HANDLE, PCWSTR, PSYMBOL_INFOW)
SymFromNameWParams = ((1, 'hProcess'), (1, 'Name'), (1, 'Symbol'))



SymLoadModuleExPrototype = WINFUNCTYPE(DWORD64, HANDLE, HANDLE, LPCSTR, LPCSTR, DWORD64, DWORD, PMODLOAD_DATA, DWORD)
SymLoadModuleExParams = ((1, 'hProcess'), (1, 'hFile'), (1, 'ImageName'), (1, 'ModuleName'), (1, 'BaseOfDll'), (1, 'DllSize'), (1, 'Data'), (1, 'Flags'))



SymSetOptionsPrototype = WINFUNCTYPE(DWORD, DWORD)
SymSetOptionsParams = ((1, 'SymOptions'),)



SymGetOptionsPrototype = WINFUNCTYPE(DWORD)
SymGetOptionsParams = ()



SymEnumSymbolsPrototype = WINFUNCTYPE(BOOL, HANDLE, ULONG64, PCSTR, PVOID, PVOID)
SymEnumSymbolsParams = ((1, 'hProcess'), (1, 'BaseOfDll'), (1, 'Mask'), (1, 'EnumSymbolsCallback'), (1, 'UserContext'))



SymEnumSymbolsExPrototype = WINFUNCTYPE(BOOL, HANDLE, ULONG64, PCSTR, PVOID, PVOID, DWORD)
SymEnumSymbolsExParams = ((1, 'hProcess'), (1, 'BaseOfDll'), (1, 'Mask'), (1, 'EnumSymbolsCallback'), (1, 'UserContext'), (1, 'Options'))



SymEnumTypesPrototype = WINFUNCTYPE(BOOL, HANDLE, ULONG64, PVOID, PVOID)
SymEnumTypesParams = ((1, 'hProcess'), (1, 'BaseOfDll'), (1, 'EnumSymbolsCallback'), (1, 'UserContext'))



SymEnumTypesByNamePrototype = WINFUNCTYPE(BOOL, HANDLE, ULONG64, PCSTR, PVOID, PVOID)
SymEnumTypesByNameParams = ((1, 'hProcess'), (1, 'BaseOfDll'), (1, 'mask'), (1, 'EnumSymbolsCallback'), (1, 'UserContext'))



SymEnumerateModules64Prototype = WINFUNCTYPE(BOOL, HANDLE, PVOID, PVOID)
SymEnumerateModules64Params = ((1, 'hProcess'), (1, 'EnumModulesCallback'), (1, 'UserContext'))



SymNextPrototype = WINFUNCTYPE(BOOL, HANDLE, PSYMBOL_INFO)
SymNextParams = ((1, 'hProcess'), (1, 'si'))



SymNextWPrototype = WINFUNCTYPE(BOOL, HANDLE, PSYMBOL_INFOW)
SymNextWParams = ((1, 'hProcess'), (1, 'siw'))



SymPrevPrototype = WINFUNCTYPE(BOOL, HANDLE, PSYMBOL_INFO)
SymPrevParams = ((1, 'hProcess'), (1, 'si'))



SymPrevWPrototype = WINFUNCTYPE(BOOL, HANDLE, PSYMBOL_INFOW)
SymPrevWParams = ((1, 'hProcess'), (1, 'siw'))



SymSetContextPrototype = WINFUNCTYPE(BOOL, HANDLE, PIMAGEHLP_STACK_FRAME, PIMAGEHLP_CONTEXT)
SymSetContextParams = ((1, 'hProcess'), (1, 'StackFrame'), (1, 'Context'))



SymSetExtendedOptionPrototype = WINFUNCTYPE(BOOL, IMAGEHLP_EXTENDED_OPTIONS, BOOL)
SymSetExtendedOptionParams = ((1, 'option'), (1, 'value'))



SymSrvGetFileIndexesPrototype = WINFUNCTYPE(BOOL, PCSTR, POINTER(GUID), PDWORD, PDWORD, DWORD)
SymSrvGetFileIndexesParams = ((1, 'File'), (1, 'Id'), (1, 'Val1'), (1, 'Val2'), (1, 'Flags'))



SymSrvGetFileIndexesWPrototype = WINFUNCTYPE(BOOL, PCWSTR, POINTER(GUID), PDWORD, PDWORD, DWORD)
SymSrvGetFileIndexesWParams = ((1, 'File'), (1, 'Id'), (1, 'Val1'), (1, 'Val2'), (1, 'Flags'))



SymSrvGetFileIndexInfoPrototype = WINFUNCTYPE(BOOL, PCSTR, PSYMSRV_INDEX_INFO, DWORD)
SymSrvGetFileIndexInfoParams = ((1, 'File'), (1, 'Info'), (1, 'Flags'))



SymSrvGetFileIndexInfoWPrototype = WINFUNCTYPE(BOOL, PCWSTR, PSYMSRV_INDEX_INFOW, DWORD)
SymSrvGetFileIndexInfoWParams = ((1, 'File'), (1, 'Info'), (1, 'Flags'))



SymSrvGetFileIndexStringPrototype = WINFUNCTYPE(BOOL, HANDLE, PCSTR, PCSTR, PSTR, SIZE_T, DWORD)
SymSrvGetFileIndexStringParams = ((1, 'hProcess'), (1, 'SrvPath'), (1, 'File'), (1, 'Index'), (1, 'Size'), (1, 'Flags'))



SymSrvGetFileIndexStringWPrototype = WINFUNCTYPE(BOOL, HANDLE, PCWSTR, PCWSTR, PWSTR, SIZE_T, DWORD)
SymSrvGetFileIndexStringWParams = ((1, 'hProcess'), (1, 'SrvPath'), (1, 'File'), (1, 'Index'), (1, 'Size'), (1, 'Flags'))



SymUnDNamePrototype = WINFUNCTYPE(BOOL, PIMAGEHLP_SYMBOL, PSTR, DWORD)
SymUnDNameParams = ((1, 'sym'), (1, 'UnDecName'), (1, 'UnDecNameLength'))



SymUnDName64Prototype = WINFUNCTYPE(BOOL, PIMAGEHLP_SYMBOL64, PSTR, DWORD)
SymUnDName64Params = ((1, 'sym'), (1, 'UnDecName'), (1, 'UnDecNameLength'))



SymUnloadModulePrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD)
SymUnloadModuleParams = ((1, 'hProcess'), (1, 'BaseOfDll'))



SymUnloadModule64Prototype = WINFUNCTYPE(BOOL, HANDLE, DWORD64)
SymUnloadModule64Params = ((1, 'hProcess'), (1, 'BaseOfDll'))



UnDecorateSymbolNamePrototype = WINFUNCTYPE(DWORD, PCSTR, PSTR, DWORD, DWORD)
UnDecorateSymbolNameParams = ((1, 'name'), (1, 'outputString'), (1, 'maxStringLength'), (1, 'flags'))



UnDecorateSymbolNameWPrototype = WINFUNCTYPE(DWORD, PCWSTR, PWSTR, DWORD, DWORD)
UnDecorateSymbolNameWParams = ((1, 'name'), (1, 'outputString'), (1, 'maxStringLength'), (1, 'flags'))



SymCleanupPrototype = WINFUNCTYPE(BOOL, HANDLE)
SymCleanupParams = ((1, 'hProcess'),)



SymEnumProcessesPrototype = WINFUNCTYPE(BOOL, PSYM_ENUMPROCESSES_CALLBACK, PVOID)
SymEnumProcessesParams = ((1, 'EnumProcessesCallback'), (1, 'UserContext'))



SymEnumSymbolsForAddrPrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD64, PSYM_ENUMERATESYMBOLS_CALLBACK, PVOID)
SymEnumSymbolsForAddrParams = ((1, 'hProcess'), (1, 'Address'), (1, 'EnumSymbolsCallback'), (1, 'UserContext'))



SymEnumSymbolsForAddrWPrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD64, PSYM_ENUMERATESYMBOLS_CALLBACKW, PVOID)
SymEnumSymbolsForAddrWParams = ((1, 'hProcess'), (1, 'Address'), (1, 'EnumSymbolsCallback'), (1, 'UserContext'))



SymGetTypeFromNamePrototype = WINFUNCTYPE(BOOL, HANDLE, ULONG64, PCSTR, PSYMBOL_INFO)
SymGetTypeFromNameParams = ((1, 'hProcess'), (1, 'BaseOfDll'), (1, 'Name'), (1, 'Symbol'))



SymGetTypeInfoPrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD64, ULONG, IMAGEHLP_SYMBOL_TYPE_INFO, PVOID)
SymGetTypeInfoParams = ((1, 'hProcess'), (1, 'ModBase'), (1, 'TypeId'), (1, 'GetType'), (1, 'pInfo'))



SymSearchPrototype = WINFUNCTYPE(BOOL, HANDLE, ULONG64, DWORD, DWORD, PCSTR, DWORD64, PSYM_ENUMERATESYMBOLS_CALLBACK, PVOID, DWORD)
SymSearchParams = ((1, 'hProcess'), (1, 'BaseOfDll'), (1, 'Index'), (1, 'SymTag'), (1, 'Mask'), (1, 'Address'), (1, 'EnumSymbolsCallback'), (1, 'UserContext'), (1, 'Options'))



SymSearchWPrototype = WINFUNCTYPE(BOOL, HANDLE, ULONG64, DWORD, DWORD, PCWSTR, DWORD64, PSYM_ENUMERATESYMBOLS_CALLBACKW, PVOID, DWORD)
SymSearchWParams = ((1, 'hProcess'), (1, 'BaseOfDll'), (1, 'Index'), (1, 'SymTag'), (1, 'Mask'), (1, 'Address'), (1, 'EnumSymbolsCallback'), (1, 'UserContext'), (1, 'Options'))



SymFunctionTableAccessPrototype = WINFUNCTYPE(PVOID, HANDLE, DWORD)
SymFunctionTableAccessParams = ((1, 'hProcess'), (1, 'AddrBase'))



SymFunctionTableAccess64Prototype = WINFUNCTYPE(PVOID, HANDLE, DWORD64)
SymFunctionTableAccess64Params = ((1, 'hProcess'), (1, 'AddrBase'))



SymGetModuleBasePrototype = WINFUNCTYPE(DWORD, HANDLE, DWORD)
SymGetModuleBaseParams = ((1, 'hProcess'), (1, 'dwAddr'))



SymGetModuleBase64Prototype = WINFUNCTYPE(DWORD64, HANDLE, DWORD64)
SymGetModuleBase64Params = ((1, 'hProcess'), (1, 'qwAddr'))



SymRefreshModuleListPrototype = WINFUNCTYPE(BOOL, HANDLE)
SymRefreshModuleListParams = ((1, 'hProcess'),)



SymRegisterCallbackPrototype = WINFUNCTYPE(BOOL, HANDLE, PSYMBOL_REGISTERED_CALLBACK, PVOID)
SymRegisterCallbackParams = ((1, 'hProcess'), (1, 'CallbackFunction'), (1, 'UserContext'))



SymRegisterCallback64Prototype = WINFUNCTYPE(BOOL, HANDLE, PSYMBOL_REGISTERED_CALLBACK64, ULONG64)
SymRegisterCallback64Params = ((1, 'hProcess'), (1, 'CallbackFunction'), (1, 'UserContext'))



SymRegisterCallbackW64Prototype = WINFUNCTYPE(BOOL, HANDLE, PSYMBOL_REGISTERED_CALLBACK64, ULONG64)
SymRegisterCallbackW64Params = ((1, 'hProcess'), (1, 'CallbackFunction'), (1, 'UserContext'))



StackWalk64Prototype = WINFUNCTYPE(BOOL, DWORD, HANDLE, HANDLE, LPSTACKFRAME64, PVOID, PREAD_PROCESS_MEMORY_ROUTINE64, PFUNCTION_TABLE_ACCESS_ROUTINE64, PGET_MODULE_BASE_ROUTINE64, PTRANSLATE_ADDRESS_ROUTINE64)
StackWalk64Params = ((1, 'MachineType'), (1, 'hProcess'), (1, 'hThread'), (1, 'StackFrame'), (1, 'ContextRecord'), (1, 'ReadMemoryRoutine'), (1, 'FunctionTableAccessRoutine'), (1, 'GetModuleBaseRoutine'), (1, 'TranslateAddress'))



StackWalkExPrototype = WINFUNCTYPE(BOOL, DWORD, HANDLE, HANDLE, LPSTACKFRAME_EX, PVOID, PREAD_PROCESS_MEMORY_ROUTINE64, PFUNCTION_TABLE_ACCESS_ROUTINE64, PGET_MODULE_BASE_ROUTINE64, PTRANSLATE_ADDRESS_ROUTINE64, DWORD)
StackWalkExParams = ((1, 'MachineType'), (1, 'hProcess'), (1, 'hThread'), (1, 'StackFrame'), (1, 'ContextRecord'), (1, 'ReadMemoryRoutine'), (1, 'FunctionTableAccessRoutine'), (1, 'GetModuleBaseRoutine'), (1, 'TranslateAddress'), (1, 'Flags'))



StackWalkPrototype = WINFUNCTYPE(BOOL, DWORD, HANDLE, HANDLE, LPSTACKFRAME, PVOID, PREAD_PROCESS_MEMORY_ROUTINE, PFUNCTION_TABLE_ACCESS_ROUTINE, PGET_MODULE_BASE_ROUTINE, PTRANSLATE_ADDRESS_ROUTINE)
StackWalkParams = ((1, 'MachineType'), (1, 'hProcess'), (1, 'hThread'), (1, 'StackFrame'), (1, 'ContextRecord'), (1, 'ReadMemoryRoutine'), (1, 'FunctionTableAccessRoutine'), (1, 'GetModuleBaseRoutine'), (1, 'TranslateAddress'))



SymGetSearchPathPrototype = WINFUNCTYPE(BOOL, HANDLE, PSTR, DWORD)
SymGetSearchPathParams = ((1, 'hProcess'), (1, 'SearchPath'), (1, 'SearchPathLength'))



SymGetSearchPathWPrototype = WINFUNCTYPE(BOOL, HANDLE, PWSTR, DWORD)
SymGetSearchPathWParams = ((1, 'hProcess'), (1, 'SearchPath'), (1, 'SearchPathLength'))



SymSetSearchPathPrototype = WINFUNCTYPE(BOOL, HANDLE, PCSTR)
SymSetSearchPathParams = ((1, 'hProcess'), (1, 'SearchPath'))



SymSetSearchPathWPrototype = WINFUNCTYPE(BOOL, HANDLE, PCWSTR)
SymSetSearchPathWParams = ((1, 'hProcess'), (1, 'SearchPath'))



CreateEventAPrototype = WINFUNCTYPE(HANDLE, LPSECURITY_ATTRIBUTES, BOOL, BOOL, LPCSTR)
CreateEventAParams = ((1, 'lpEventAttributes'), (1, 'bManualReset'), (1, 'bInitialState'), (1, 'lpName'))



CreateEventWPrototype = WINFUNCTYPE(HANDLE, LPSECURITY_ATTRIBUTES, BOOL, BOOL, LPCWSTR)
CreateEventWParams = ((1, 'lpEventAttributes'), (1, 'bManualReset'), (1, 'bInitialState'), (1, 'lpName'))



CreateEventExAPrototype = WINFUNCTYPE(HANDLE, LPSECURITY_ATTRIBUTES, LPCSTR, DWORD, DWORD)
CreateEventExAParams = ((1, 'lpEventAttributes'), (1, 'lpName'), (1, 'dwFlags'), (1, 'dwDesiredAccess'))



CreateEventExWPrototype = WINFUNCTYPE(HANDLE, LPSECURITY_ATTRIBUTES, LPCWSTR, DWORD, DWORD)
CreateEventExWParams = ((1, 'lpEventAttributes'), (1, 'lpName'), (1, 'dwFlags'), (1, 'dwDesiredAccess'))



OpenEventAPrototype = WINFUNCTYPE(HANDLE, DWORD, BOOL, LPCSTR)
OpenEventAParams = ((1, 'dwDesiredAccess'), (1, 'bInheritHandle'), (1, 'lpName'))



OpenEventWPrototype = WINFUNCTYPE(HANDLE, DWORD, BOOL, LPCWSTR)
OpenEventWParams = ((1, 'dwDesiredAccess'), (1, 'bInheritHandle'), (1, 'lpName'))



NtQueryLicenseValuePrototype = WINFUNCTYPE(NTSTATUS, PUNICODE_STRING, POINTER(ULONG), PVOID, ULONG, POINTER(ULONG))
NtQueryLicenseValueParams = ((1, 'Name'), (1, 'Type'), (1, 'Buffer'), (1, 'Length'), (1, 'DataLength'))



NtQueryEaFilePrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PIO_STATUS_BLOCK, PVOID, ULONG, BOOLEAN, PVOID, ULONG, PULONG, BOOLEAN)
NtQueryEaFileParams = ((1, 'FileHandle'), (1, 'IoStatusBlock'), (1, 'Buffer'), (1, 'Length'), (1, 'ReturnSingleEntry'), (1, 'EaList'), (1, 'EaListLength'), (1, 'EaIndex'), (1, 'RestartScan'))



NtSetEaFilePrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PIO_STATUS_BLOCK, PVOID, ULONG)
NtSetEaFileParams = ((1, 'FileHandle'), (1, 'IoStatusBlock'), (1, 'Buffer'), (1, 'Length'))



NtCreateProcessExPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, HANDLE, ULONG, HANDLE, HANDLE, HANDLE, BOOLEAN)
NtCreateProcessExParams = ((1, 'ProcessHandle'), (1, 'DesiredAccess'), (1, 'ObjectAttributes'), (1, 'ParentProcess'), (1, 'Flags'), (1, 'SectionHandle'), (1, 'DebugPort'), (1, 'ExceptionPort'), (1, 'InJob'))



NtCreateNamedPipeFilePrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PIO_STATUS_BLOCK, ULONG, ULONG, ULONG, BOOLEAN, BOOLEAN, BOOLEAN, ULONG, ULONG, ULONG, PLARGE_INTEGER)
NtCreateNamedPipeFileParams = ((1, 'NamedPipeFileHandle'), (1, 'DesiredAccess'), (1, 'ObjectAttributes'), (1, 'IoStatusBlock'), (1, 'ShareAccess'), (1, 'CreateDisposition'), (1, 'CreateOptions'), (1, 'WriteModeMessage'), (1, 'ReadModeMessage'), (1, 'NonBlocking'), (1, 'MaxInstances'), (1, 'InBufferSize'), (1, 'OutBufferSize'), (1, 'DefaultTimeOut'))



NtCreateFilePrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PIO_STATUS_BLOCK, PLARGE_INTEGER, ULONG, ULONG, ULONG, ULONG, PVOID, ULONG)
NtCreateFileParams = ((1, 'FileHandle'), (1, 'DesiredAccess'), (1, 'ObjectAttributes'), (1, 'IoStatusBlock'), (1, 'AllocationSize'), (1, 'FileAttributes'), (1, 'ShareAccess'), (1, 'CreateDisposition'), (1, 'CreateOptions'), (1, 'EaBuffer'), (1, 'EaLength'))



NtOpenFilePrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PIO_STATUS_BLOCK, ULONG, ULONG)
NtOpenFileParams = ((1, 'FileHandle'), (1, 'DesiredAccess'), (1, 'ObjectAttributes'), (1, 'IoStatusBlock'), (1, 'ShareAccess'), (1, 'OpenOptions'))



NtCreateSymbolicLinkObjectPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PUNICODE_STRING)
NtCreateSymbolicLinkObjectParams = ((1, 'pHandle'), (1, 'DesiredAccess'), (1, 'ObjectAttributes'), (1, 'DestinationName'))



NtSetInformationProcessPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PROCESSINFOCLASS, PVOID, ULONG)
NtSetInformationProcessParams = ((1, 'ProcessHandle'), (1, 'ProcessInformationClass'), (1, 'ProcessInformation'), (1, 'ProcessInformationLength'))



NtQueryVirtualMemoryPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PVOID, MEMORY_INFORMATION_CLASS, PVOID, SIZE_T, PSIZE_T)
NtQueryVirtualMemoryParams = ((1, 'ProcessHandle'), (1, 'BaseAddress'), (1, 'MemoryInformationClass'), (1, 'MemoryInformation'), (1, 'MemoryInformationLength'), (1, 'ReturnLength'))



NtQueryVolumeInformationFilePrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PIO_STATUS_BLOCK, PVOID, ULONG, FS_INFORMATION_CLASS)
NtQueryVolumeInformationFileParams = ((1, 'FileHandle'), (1, 'IoStatusBlock'), (1, 'FsInformation'), (1, 'Length'), (1, 'FsInformationClass'))



NtCreateThreadExPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, ACCESS_MASK, LPVOID, HANDLE, LPTHREAD_START_ROUTINE, LPVOID, BOOL, DWORD, DWORD, DWORD, LPVOID)
NtCreateThreadExParams = ((1, 'ThreadHandle'), (1, 'DesiredAccess'), (1, 'ObjectAttributes'), (1, 'ProcessHandle'), (1, 'lpStartAddress'), (1, 'lpParameter'), (1, 'CreateSuspended'), (1, 'dwStackSize'), (1, 'Unknown1'), (1, 'Unknown2'), (1, 'Unknown3'))



NtGetContextThreadPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, LPCONTEXT)
NtGetContextThreadParams = ((1, 'hThread'), (1, 'lpContext'))



NtSetContextThreadPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, LPCONTEXT)
NtSetContextThreadParams = ((1, 'hThread'), (1, 'lpContext'))



NtQueryInformationThreadPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, THREAD_INFORMATION_CLASS, PVOID, ULONG, PULONG)
NtQueryInformationThreadParams = ((1, 'ThreadHandle'), (1, 'ThreadInformationClass'), (1, 'ThreadInformation'), (1, 'ThreadInformationLength'), (1, 'ReturnLength'))



NtAllocateVirtualMemoryPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, POINTER(PVOID), ULONG_PTR, PSIZE_T, ULONG, ULONG)
NtAllocateVirtualMemoryParams = ((1, 'ProcessHandle'), (1, 'BaseAddress'), (1, 'ZeroBits'), (1, 'RegionSize'), (1, 'AllocationType'), (1, 'Protect'))



NtProtectVirtualMemoryPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, POINTER(PVOID), PULONG, ULONG, PULONG)
NtProtectVirtualMemoryParams = ((1, 'ProcessHandle'), (1, 'BaseAddress'), (1, 'NumberOfBytesToProtect'), (1, 'NewAccessProtection'), (1, 'OldAccessProtection'))



NtQuerySystemInformationPrototype = WINFUNCTYPE(NTSTATUS, SYSTEM_INFORMATION_CLASS, PVOID, ULONG, PULONG)
NtQuerySystemInformationParams = ((1, 'SystemInformationClass'), (1, 'SystemInformation'), (1, 'SystemInformationLength'), (1, 'ReturnLength'))



NtQueryInformationProcessPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PROCESSINFOCLASS, PVOID, ULONG, PULONG)
NtQueryInformationProcessParams = ((1, 'ProcessHandle'), (1, 'ProcessInformationClass'), (1, 'ProcessInformation'), (1, 'ProcessInformationLength'), (1, 'ReturnLength'))



NtReadVirtualMemoryPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PVOID, LPVOID, ULONG, PULONG)
NtReadVirtualMemoryParams = ((1, 'hProcess'), (1, 'lpBaseAddress'), (1, 'lpBuffer'), (1, 'nSize'), (1, 'lpNumberOfBytesRead'))



NtWriteVirtualMemoryPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PVOID, PVOID, ULONG, PULONG)
NtWriteVirtualMemoryParams = ((1, 'ProcessHandle'), (1, 'BaseAddress'), (1, 'Buffer'), (1, 'NumberOfBytesToWrite'), (1, 'NumberOfBytesWritten'))



NtOpenEventPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES)
NtOpenEventParams = ((1, 'EventHandle'), (1, 'DesiredAccess'), (1, 'ObjectAttributes'))



NtQueryObjectPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, OBJECT_INFORMATION_CLASS, PVOID, ULONG, PULONG)
NtQueryObjectParams = ((1, 'Handle'), (1, 'ObjectInformationClass'), (1, 'ObjectInformation'), (1, 'ObjectInformationLength'), (1, 'ReturnLength'))



NtOpenDirectoryObjectPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES)
NtOpenDirectoryObjectParams = ((1, 'DirectoryHandle'), (1, 'DesiredAccess'), (1, 'ObjectAttributes'))



NtQueryDirectoryObjectPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PVOID, ULONG, BOOLEAN, BOOLEAN, PULONG, PULONG)
NtQueryDirectoryObjectParams = ((1, 'DirectoryHandle'), (1, 'Buffer'), (1, 'Length'), (1, 'ReturnSingleEntry'), (1, 'RestartScan'), (1, 'Context'), (1, 'ReturnLength'))



NtQuerySymbolicLinkObjectPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PUNICODE_STRING, PULONG)
NtQuerySymbolicLinkObjectParams = ((1, 'LinkHandle'), (1, 'LinkTarget'), (1, 'ReturnedLength'))



NtOpenSymbolicLinkObjectPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES)
NtOpenSymbolicLinkObjectParams = ((1, 'LinkHandle'), (1, 'DesiredAccess'), (1, 'ObjectAttributes'))



NtQueryInformationFilePrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PIO_STATUS_BLOCK, PVOID, ULONG, FILE_INFORMATION_CLASS)
NtQueryInformationFileParams = ((1, 'FileHandle'), (1, 'IoStatusBlock'), (1, 'FileInformation'), (1, 'Length'), (1, 'FileInformationClass'))



NtQueryDirectoryFilePrototype = WINFUNCTYPE(NTSTATUS, HANDLE, HANDLE, PIO_APC_ROUTINE, PVOID, PIO_STATUS_BLOCK, PVOID, ULONG, FILE_INFORMATION_CLASS, BOOLEAN, PUNICODE_STRING, BOOLEAN)
NtQueryDirectoryFileParams = ((1, 'FileHandle'), (1, 'Event'), (1, 'ApcRoutine'), (1, 'ApcContext'), (1, 'IoStatusBlock'), (1, 'FileInformation'), (1, 'Length'), (1, 'FileInformationClass'), (1, 'ReturnSingleEntry'), (1, 'FileName'), (1, 'RestartScan'))



NtSetInformationFilePrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PIO_STATUS_BLOCK, PVOID, ULONG, FILE_INFORMATION_CLASS)
NtSetInformationFileParams = ((1, 'FileHandle'), (1, 'IoStatusBlock'), (1, 'FileInformation'), (1, 'Length'), (1, 'FileInformationClass'))



NtEnumerateSystemEnvironmentValuesExPrototype = WINFUNCTYPE(NTSTATUS, ULONG, PVOID, ULONG)
NtEnumerateSystemEnvironmentValuesExParams = ((1, 'InformationClass'), (1, 'Buffer'), (1, 'BufferLength'))



NtFreeVirtualMemoryPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, POINTER(PVOID), PSIZE_T, ULONG)
NtFreeVirtualMemoryParams = ((1, 'ProcessHandle'), (1, 'BaseAddress'), (1, 'RegionSize'), (1, 'FreeType'))



NtGetContextThreadPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, LPCONTEXT)
NtGetContextThreadParams = ((1, 'hThread'), (1, 'lpContext'))



NtSetContextThreadPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, LPCONTEXT)
NtSetContextThreadParams = ((1, 'hThread'), (1, 'lpContext'))



NtCreateSectionPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PLARGE_INTEGER, ULONG, ULONG, HANDLE)
NtCreateSectionParams = ((1, 'SectionHandle'), (1, 'DesiredAccess'), (1, 'ObjectAttributes'), (1, 'MaximumSize'), (1, 'SectionPageProtection'), (1, 'AllocationAttributes'), (1, 'FileHandle'))



NtOpenSectionPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES)
NtOpenSectionParams = ((1, 'SectionHandle'), (1, 'DesiredAccess'), (1, 'ObjectAttributes'))



NtMapViewOfSectionPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, HANDLE, POINTER(PVOID), ULONG_PTR, SIZE_T, PLARGE_INTEGER, PSIZE_T, SECTION_INHERIT, ULONG, ULONG)
NtMapViewOfSectionParams = ((1, 'SectionHandle'), (1, 'ProcessHandle'), (1, 'BaseAddress'), (1, 'ZeroBits'), (1, 'CommitSize'), (1, 'SectionOffset'), (1, 'ViewSize'), (1, 'InheritDisposition'), (1, 'AllocationType'), (1, 'Win32Protect'))



NtUnmapViewOfSectionPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, PVOID)
NtUnmapViewOfSectionParams = ((1, 'ProcessHandle'), (1, 'BaseAddress'))



NtOpenProcessPrototype = WINFUNCTYPE(NTSTATUS, PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PCLIENT_ID)
NtOpenProcessParams = ((1, 'ProcessHandle'), (1, 'DesiredAccess'), (1, 'ObjectAttributes'), (1, 'ClientId'))



NtDelayExecutionPrototype = WINFUNCTYPE(NTSTATUS, BOOLEAN, PLARGE_INTEGER)
NtDelayExecutionParams = ((1, 'Alertable'), (1, 'DelayInterval'))



NtTerminateProcessPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, NTSTATUS)
NtTerminateProcessParams = ((1, 'ProcessHandle'), (1, 'ExitStatus'))



GetComputerNameExAPrototype = WINFUNCTYPE(BOOL, COMPUTER_NAME_FORMAT, LPSTR, LPDWORD)
GetComputerNameExAParams = ((1, 'NameType'), (1, 'lpBuffer'), (1, 'nSize'))



GetComputerNameExWPrototype = WINFUNCTYPE(BOOL, COMPUTER_NAME_FORMAT, LPWSTR, LPDWORD)
GetComputerNameExWParams = ((1, 'NameType'), (1, 'lpBuffer'), (1, 'nSize'))



GetComputerNameAPrototype = WINFUNCTYPE(BOOL, LPCSTR, LPDWORD)
GetComputerNameAParams = ((1, 'lpBuffer'), (1, 'lpnSize'))



GetComputerNameWPrototype = WINFUNCTYPE(BOOL, LPWSTR, LPDWORD)
GetComputerNameWParams = ((1, 'lpBuffer'), (1, 'lpnSize'))



LookupAccountSidAPrototype = WINFUNCTYPE(BOOL, LPCSTR, PSID, LPCSTR, LPDWORD, LPCSTR, LPDWORD, PSID_NAME_USE)
LookupAccountSidAParams = ((1, 'lpSystemName'), (1, 'lpSid'), (1, 'lpName'), (1, 'cchName'), (1, 'lpReferencedDomainName'), (1, 'cchReferencedDomainName'), (1, 'peUse'))



LookupAccountSidWPrototype = WINFUNCTYPE(BOOL, LPWSTR, PSID, LPWSTR, LPDWORD, LPWSTR, LPDWORD, PSID_NAME_USE)
LookupAccountSidWParams = ((1, 'lpSystemName'), (1, 'lpSid'), (1, 'lpName'), (1, 'cchName'), (1, 'lpReferencedDomainName'), (1, 'cchReferencedDomainName'), (1, 'peUse'))



LookupAccountNameAPrototype = WINFUNCTYPE(BOOL, LPCSTR, LPCSTR, PSID, LPDWORD, LPSTR, LPDWORD, PSID_NAME_USE)
LookupAccountNameAParams = ((1, 'lpSystemName'), (1, 'lpAccountName'), (1, 'Sid'), (1, 'cbSid'), (1, 'ReferencedDomainName'), (1, 'cchReferencedDomainName'), (1, 'peUse'))



LookupAccountNameWPrototype = WINFUNCTYPE(BOOL, LPCWSTR, LPCWSTR, PSID, LPDWORD, LPWSTR, LPDWORD, PSID_NAME_USE)
LookupAccountNameWParams = ((1, 'lpSystemName'), (1, 'lpAccountName'), (1, 'Sid'), (1, 'cbSid'), (1, 'ReferencedDomainName'), (1, 'cchReferencedDomainName'), (1, 'peUse'))



FileTimeToSystemTimePrototype = WINFUNCTYPE(BOOL, POINTER(FILETIME), LPSYSTEMTIME)
FileTimeToSystemTimeParams = ((1, 'lpFileTime'), (1, 'lpSystemTime'))



SystemTimeToFileTimePrototype = WINFUNCTYPE(BOOL, POINTER(SYSTEMTIME), LPFILETIME)
SystemTimeToFileTimeParams = ((1, 'lpSystemTime'), (1, 'lpFileTime'))



GetSystemTimePrototype = WINFUNCTYPE(PVOID, LPSYSTEMTIME)
GetSystemTimeParams = ((1, 'lpSystemTime'),)



GetSystemTimesPrototype = WINFUNCTYPE(BOOL, PFILETIME, PFILETIME, PFILETIME)
GetSystemTimesParams = ((1, 'lpIdleTime'), (1, 'lpKernelTime'), (1, 'lpUserTime'))



GetSystemTimeAsFileTimePrototype = WINFUNCTYPE(PVOID, LPFILETIME)
GetSystemTimeAsFileTimeParams = ((1, 'lpSystemTimeAsFileTime'),)



GetLocalTimePrototype = WINFUNCTYPE(PVOID, LPSYSTEMTIME)
GetLocalTimeParams = ((1, 'lpSystemTime'),)



GetTickCountPrototype = WINFUNCTYPE(DWORD)
GetTickCountParams = ()



GetTickCount64Prototype = WINFUNCTYPE(ULONGLONG)
GetTickCount64Params = ()



TdhEnumerateProvidersPrototype = WINFUNCTYPE(TDHSTATUS, PPROVIDER_ENUMERATION_INFO, POINTER(ULONG))
TdhEnumerateProvidersParams = ((1, 'pBuffer'), (1, 'pBufferSize'))



GetFileVersionInfoAPrototype = WINFUNCTYPE(BOOL, LPCSTR, DWORD, DWORD, LPVOID)
GetFileVersionInfoAParams = ((1, 'lptstrFilename'), (1, 'dwHandle'), (1, 'dwLen'), (1, 'lpData'))



GetFileVersionInfoWPrototype = WINFUNCTYPE(BOOL, LPWSTR, DWORD, DWORD, LPVOID)
GetFileVersionInfoWParams = ((1, 'lptstrFilename'), (1, 'dwHandle'), (1, 'dwLen'), (1, 'lpData'))



GetFileVersionInfoExAPrototype = WINFUNCTYPE(BOOL, DWORD, LPCSTR, DWORD, DWORD, LPVOID)
GetFileVersionInfoExAParams = ((1, 'dwFlags'), (1, 'lpwstrFilename'), (1, 'dwHandle'), (1, 'dwLen'), (1, 'lpData'))



GetFileVersionInfoExWPrototype = WINFUNCTYPE(BOOL, DWORD, LPCWSTR, DWORD, DWORD, LPVOID)
GetFileVersionInfoExWParams = ((1, 'dwFlags'), (1, 'lpwstrFilename'), (1, 'dwHandle'), (1, 'dwLen'), (1, 'lpData'))



GetFileVersionInfoSizeAPrototype = WINFUNCTYPE(DWORD, LPCSTR, LPDWORD)
GetFileVersionInfoSizeAParams = ((1, 'lptstrFilename'), (1, 'lpdwHandle'))



GetFileVersionInfoSizeWPrototype = WINFUNCTYPE(DWORD, LPWSTR, LPDWORD)
GetFileVersionInfoSizeWParams = ((1, 'lptstrFilename'), (1, 'lpdwHandle'))



GetFileVersionInfoSizeExAPrototype = WINFUNCTYPE(DWORD, DWORD, LPCSTR, LPDWORD)
GetFileVersionInfoSizeExAParams = ((1, 'dwFlags'), (1, 'lpwstrFilename'), (1, 'lpdwHandle'))



GetFileVersionInfoSizeExWPrototype = WINFUNCTYPE(DWORD, DWORD, LPCWSTR, LPDWORD)
GetFileVersionInfoSizeExWParams = ((1, 'dwFlags'), (1, 'lpwstrFilename'), (1, 'lpdwHandle'))



VerQueryValueAPrototype = WINFUNCTYPE(BOOL, LPCVOID, LPCSTR, POINTER(LPVOID), PUINT)
VerQueryValueAParams = ((1, 'pBlock'), (1, 'lpSubBlock'), (1, 'lplpBuffer'), (1, 'puLen'))



VerQueryValueWPrototype = WINFUNCTYPE(BOOL, LPCVOID, LPWSTR, POINTER(LPVOID), PUINT)
VerQueryValueWParams = ((1, 'pBlock'), (1, 'lpSubBlock'), (1, 'lplpBuffer'), (1, 'puLen'))



GetCursorPosPrototype = WINFUNCTYPE(BOOL, LPPOINT)
GetCursorPosParams = ((1, 'lpPoint'),)



WindowFromPointPrototype = WINFUNCTYPE(HWND, POINT)
WindowFromPointParams = ((1, 'Point'),)



GetWindowRectPrototype = WINFUNCTYPE(BOOL, HWND, LPRECT)
GetWindowRectParams = ((1, 'hWnd'), (1, 'lpRect'))



EnumWindowsPrototype = WINFUNCTYPE(BOOL, WNDENUMPROC, LPARAM)
EnumWindowsParams = ((1, 'lpEnumFunc'), (1, 'lParam'))



GetWindowTextAPrototype = WINFUNCTYPE(INT, HWND, LPSTR, INT)
GetWindowTextAParams = ((1, 'hWnd'), (1, 'lpString'), (1, 'nMaxCount'))



GetParentPrototype = WINFUNCTYPE(HWND, HWND)
GetParentParams = ((1, 'hWnd'),)



GetWindowTextWPrototype = WINFUNCTYPE(INT, HWND, LPWSTR, INT)
GetWindowTextWParams = ((1, 'hWnd'), (1, 'lpString'), (1, 'nMaxCount'))



GetWindowModuleFileNameAPrototype = WINFUNCTYPE(UINT, HWND, LPSTR, UINT)
GetWindowModuleFileNameAParams = ((1, 'hwnd'), (1, 'pszFileName'), (1, 'cchFileNameMax'))



GetWindowModuleFileNameWPrototype = WINFUNCTYPE(UINT, HWND, LPWSTR, UINT)
GetWindowModuleFileNameWParams = ((1, 'hwnd'), (1, 'pszFileName'), (1, 'cchFileNameMax'))



EnumChildWindowsPrototype = WINFUNCTYPE(BOOL, HWND, WNDENUMPROC, LPARAM)
EnumChildWindowsParams = ((1, 'hWndParent'), (1, 'lpEnumFunc'), (1, 'lParam'))



CloseWindowPrototype = WINFUNCTYPE(BOOL, HWND)
CloseWindowParams = ((1, 'hWnd'),)



GetDesktopWindowPrototype = WINFUNCTYPE(HWND)
GetDesktopWindowParams = ()



GetForegroundWindowPrototype = WINFUNCTYPE(HWND)
GetForegroundWindowParams = ()



BringWindowToTopPrototype = WINFUNCTYPE(BOOL, HWND)
BringWindowToTopParams = ((1, 'hWnd'),)



MoveWindowPrototype = WINFUNCTYPE(BOOL, HWND, INT, INT, INT, INT, BOOL)
MoveWindowParams = ((1, 'hWnd'), (1, 'X'), (1, 'Y'), (1, 'nWidth'), (1, 'nHeight'), (1, 'bRepaint'))



SetWindowPosPrototype = WINFUNCTYPE(BOOL, HWND, HWND, INT, INT, INT, INT, UINT)
SetWindowPosParams = ((1, 'hWnd'), (1, 'hWndInsertAfter'), (1, 'X'), (1, 'Y'), (1, 'cx'), (1, 'cy'), (1, 'uFlags'))



SetWindowTextAPrototype = WINFUNCTYPE(BOOL, HWND, LPCSTR)
SetWindowTextAParams = ((1, 'hWnd'), (1, 'lpString'))



SetWindowTextWPrototype = WINFUNCTYPE(BOOL, HWND, LPWSTR)
SetWindowTextWParams = ((1, 'hWnd'), (1, 'lpString'))



RealGetWindowClassAPrototype = WINFUNCTYPE(UINT, HWND, LPCSTR, UINT)
RealGetWindowClassAParams = ((1, 'hwnd'), (1, 'pszType'), (1, 'cchType'))



RealGetWindowClassWPrototype = WINFUNCTYPE(UINT, HWND, LPWSTR, UINT)
RealGetWindowClassWParams = ((1, 'hwnd'), (1, 'pszType'), (1, 'cchType'))



GetClassInfoExAPrototype = WINFUNCTYPE(BOOL, HINSTANCE, LPCSTR, LPWNDCLASSEXA)
GetClassInfoExAParams = ((1, 'hinst'), (1, 'lpszClass'), (1, 'lpwcx'))



GetClassInfoExWPrototype = WINFUNCTYPE(BOOL, HINSTANCE, LPCWSTR, LPWNDCLASSEXW)
GetClassInfoExWParams = ((1, 'hinst'), (1, 'lpszClass'), (1, 'lpwcx'))



GetClassNameAPrototype = WINFUNCTYPE(INT, HWND, LPCSTR, INT)
GetClassNameAParams = ((1, 'hWnd'), (1, 'lpClassName'), (1, 'nMaxCount'))



GetClassNameWPrototype = WINFUNCTYPE(INT, HWND, LPWSTR, INT)
GetClassNameWParams = ((1, 'hWnd'), (1, 'lpClassName'), (1, 'nMaxCount'))



GetWindowThreadProcessIdPrototype = WINFUNCTYPE(DWORD, HWND, LPDWORD)
GetWindowThreadProcessIdParams = ((1, 'hWnd'), (1, 'lpdwProcessId'))



FindWindowAPrototype = WINFUNCTYPE(HWND, LPCSTR, LPCSTR)
FindWindowAParams = ((1, 'lpClassName'), (1, 'lpWindowName'))



FindWindowWPrototype = WINFUNCTYPE(HWND, LPCWSTR, LPCWSTR)
FindWindowWParams = ((1, 'lpClassName'), (1, 'lpWindowName'))



ExitProcessPrototype = WINFUNCTYPE(VOID, UINT)
ExitProcessParams = ((1, 'uExitCode'),)



TerminateProcessPrototype = WINFUNCTYPE(BOOL, HANDLE, UINT)
TerminateProcessParams = ((1, 'hProcess'), (1, 'uExitCode'))



GetLastErrorPrototype = WINFUNCTYPE(DWORD)
GetLastErrorParams = ()



LdrLoadDllPrototype = WINFUNCTYPE(NTSTATUS, LPCWSTR, PVOID, PUNICODE_STRING, PHANDLE)
LdrLoadDllParams = ((1, 'PathToFile'), (1, 'Flags'), (1, 'ModuleFileName'), (1, 'ModuleHandle'))



GetExitCodeThreadPrototype = WINFUNCTYPE(BOOL, HANDLE, LPDWORD)
GetExitCodeThreadParams = ((1, 'hThread'), (1, 'lpExitCode'))



GetExitCodeProcessPrototype = WINFUNCTYPE(BOOL, HANDLE, LPDWORD)
GetExitCodeProcessParams = ((1, 'hProcess'), (1, 'lpExitCode'))



SetPriorityClassPrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD)
SetPriorityClassParams = ((1, 'hProcess'), (1, 'dwPriorityClass'))



GetPriorityClassPrototype = WINFUNCTYPE(DWORD, HANDLE)
GetPriorityClassParams = ((1, 'hProcess'),)



VirtualAllocPrototype = WINFUNCTYPE(LPVOID, LPVOID, SIZE_T, DWORD, DWORD)
VirtualAllocParams = ((1, 'lpAddress'), (1, 'dwSize'), (1, 'flAllocationType'), (1, 'flProtect'))



VirtualAllocExPrototype = WINFUNCTYPE(LPVOID, HANDLE, LPVOID, SIZE_T, DWORD, DWORD)
VirtualAllocExParams = ((1, 'hProcess'), (1, 'lpAddress'), (1, 'dwSize'), (1, 'flAllocationType'), (1, 'flProtect'))



VirtualFreePrototype = WINFUNCTYPE(BOOL, LPVOID, SIZE_T, DWORD)
VirtualFreeParams = ((1, 'lpAddress'), (1, 'dwSize'), (1, 'dwFreeType'))



VirtualFreeExPrototype = WINFUNCTYPE(BOOL, HANDLE, LPVOID, SIZE_T, DWORD)
VirtualFreeExParams = ((1, 'hProcess'), (1, 'lpAddress'), (1, 'dwSize'), (1, 'dwFreeType'))



VirtualProtectPrototype = WINFUNCTYPE(BOOL, LPVOID, SIZE_T, DWORD, PDWORD)
VirtualProtectParams = ((1, 'lpAddress'), (1, 'dwSize'), (1, 'flNewProtect'), (1, 'lpflOldProtect'))



VirtualProtectExPrototype = WINFUNCTYPE(BOOL, HANDLE, LPVOID, SIZE_T, DWORD, PDWORD)
VirtualProtectExParams = ((1, 'hProcess'), (1, 'lpAddress'), (1, 'dwSize'), (1, 'flNewProtect'), (1, 'lpflOldProtect'))



VirtualQueryPrototype = WINFUNCTYPE(DWORD, LPCVOID, PMEMORY_BASIC_INFORMATION, DWORD)
VirtualQueryParams = ((1, 'lpAddress'), (1, 'lpBuffer'), (1, 'dwLength'))



VirtualQueryExPrototype = WINFUNCTYPE(SIZE_T, HANDLE, LPCVOID, PMEMORY_BASIC_INFORMATION, SIZE_T)
VirtualQueryExParams = ((1, 'hProcess'), (1, 'lpAddress'), (1, 'lpBuffer'), (1, 'dwLength'))



QueryWorkingSetPrototype = WINFUNCTYPE(BOOL, HANDLE, PVOID, DWORD)
QueryWorkingSetParams = ((1, 'hProcess'), (1, 'pv'), (1, 'cb'))



QueryWorkingSetExPrototype = WINFUNCTYPE(BOOL, HANDLE, PVOID, DWORD)
QueryWorkingSetExParams = ((1, 'hProcess'), (1, 'pv'), (1, 'cb'))



GetModuleFileNameAPrototype = WINFUNCTYPE(DWORD, HMODULE, LPSTR, DWORD)
GetModuleFileNameAParams = ((1, 'hModule'), (1, 'lpFilename'), (1, 'nSize'))



GetModuleFileNameWPrototype = WINFUNCTYPE(DWORD, HMODULE, LPWSTR, DWORD)
GetModuleFileNameWParams = ((1, 'hModule'), (1, 'lpFilename'), (1, 'nSize'))



CreateThreadPrototype = WINFUNCTYPE(HANDLE, LPSECURITY_ATTRIBUTES, SIZE_T, LPTHREAD_START_ROUTINE, LPVOID, DWORD, LPDWORD)
CreateThreadParams = ((1, 'lpThreadAttributes'), (1, 'dwStackSize'), (1, 'lpStartAddress'), (1, 'lpParameter'), (1, 'dwCreationFlags'), (1, 'lpThreadId'))



CreateRemoteThreadPrototype = WINFUNCTYPE(HANDLE, HANDLE, LPSECURITY_ATTRIBUTES, SIZE_T, LPTHREAD_START_ROUTINE, LPVOID, DWORD, LPDWORD)
CreateRemoteThreadParams = ((1, 'hProcess'), (1, 'lpThreadAttributes'), (1, 'dwStackSize'), (1, 'lpStartAddress'), (1, 'lpParameter'), (1, 'dwCreationFlags'), (1, 'lpThreadId'))



VirtualProtectPrototype = WINFUNCTYPE(BOOL, LPVOID, SIZE_T, DWORD, PDWORD)
VirtualProtectParams = ((1, 'lpAddress'), (1, 'dwSize'), (1, 'flNewProtect'), (1, 'lpflOldProtect'))



CreateProcessAPrototype = WINFUNCTYPE(BOOL, LPCSTR, LPSTR, LPSECURITY_ATTRIBUTES, LPSECURITY_ATTRIBUTES, BOOL, DWORD, LPVOID, LPCSTR, LPSTARTUPINFOA, LPPROCESS_INFORMATION)
CreateProcessAParams = ((1, 'lpApplicationName'), (1, 'lpCommandLine'), (1, 'lpProcessAttributes'), (1, 'lpThreadAttributes'), (1, 'bInheritHandles'), (1, 'dwCreationFlags'), (1, 'lpEnvironment'), (1, 'lpCurrentDirectory'), (1, 'lpStartupInfo'), (1, 'lpProcessInformation'))



CreateProcessWPrototype = WINFUNCTYPE(BOOL, LPCWSTR, LPWSTR, LPSECURITY_ATTRIBUTES, LPSECURITY_ATTRIBUTES, BOOL, DWORD, LPVOID, LPCWSTR, LPSTARTUPINFOW, LPPROCESS_INFORMATION)
CreateProcessWParams = ((1, 'lpApplicationName'), (1, 'lpCommandLine'), (1, 'lpProcessAttributes'), (1, 'lpThreadAttributes'), (1, 'bInheritHandles'), (1, 'dwCreationFlags'), (1, 'lpEnvironment'), (1, 'lpCurrentDirectory'), (1, 'lpStartupInfo'), (1, 'lpProcessInformation'))



CreateProcessAsUserAPrototype = WINFUNCTYPE(BOOL, HANDLE, LPSTR, LPSTR, LPSECURITY_ATTRIBUTES, LPSECURITY_ATTRIBUTES, BOOL, DWORD, LPVOID, LPSTR, LPSTARTUPINFOA, LPPROCESS_INFORMATION)
CreateProcessAsUserAParams = ((1, 'hToken'), (1, 'lpApplicationName'), (1, 'lpCommandLine'), (1, 'lpProcessAttributes'), (1, 'lpThreadAttributes'), (1, 'bInheritHandles'), (1, 'dwCreationFlags'), (1, 'lpEnvironment'), (1, 'lpCurrentDirectory'), (1, 'lpStartupInfo'), (1, 'lpProcessInformation'))



CreateProcessAsUserWPrototype = WINFUNCTYPE(BOOL, HANDLE, LPWSTR, LPWSTR, LPSECURITY_ATTRIBUTES, LPSECURITY_ATTRIBUTES, BOOL, DWORD, LPVOID, LPWSTR, LPSTARTUPINFOW, LPPROCESS_INFORMATION)
CreateProcessAsUserWParams = ((1, 'hToken'), (1, 'lpApplicationName'), (1, 'lpCommandLine'), (1, 'lpProcessAttributes'), (1, 'lpThreadAttributes'), (1, 'bInheritHandles'), (1, 'dwCreationFlags'), (1, 'lpEnvironment'), (1, 'lpCurrentDirectory'), (1, 'lpStartupInfo'), (1, 'lpProcessInformation'))



GetThreadContextPrototype = WINFUNCTYPE(BOOL, HANDLE, LPCONTEXT)
GetThreadContextParams = ((1, 'hThread'), (1, 'lpContext'))



SetThreadContextPrototype = WINFUNCTYPE(BOOL, HANDLE, LPCONTEXT)
SetThreadContextParams = ((1, 'hThread'), (1, 'lpContext'))



OpenThreadPrototype = WINFUNCTYPE(HANDLE, DWORD, BOOL, DWORD)
OpenThreadParams = ((1, 'dwDesiredAccess'), (1, 'bInheritHandle'), (1, 'dwThreadId'))



OpenProcessPrototype = WINFUNCTYPE(HANDLE, DWORD, BOOL, DWORD)
OpenProcessParams = ((1, 'dwDesiredAccess'), (1, 'bInheritHandle'), (1, 'dwProcessId'))



CloseHandlePrototype = WINFUNCTYPE(BOOL, HANDLE)
CloseHandleParams = ((1, 'hObject'),)



ReadProcessMemoryPrototype = WINFUNCTYPE(BOOL, HANDLE, LPCVOID, LPVOID, SIZE_T, POINTER(SIZE_T))
ReadProcessMemoryParams = ((1, 'hProcess'), (1, 'lpBaseAddress'), (1, 'lpBuffer'), (1, 'nSize'), (1, 'lpNumberOfBytesRead'))



NtWow64ReadVirtualMemory64Prototype = WINFUNCTYPE(NTSTATUS, HANDLE, ULONG64, LPVOID, ULONG64, PULONG64)
NtWow64ReadVirtualMemory64Params = ((1, 'hProcess'), (1, 'lpBaseAddress'), (1, 'lpBuffer'), (1, 'nSize'), (1, 'lpNumberOfBytesRead'))



WriteProcessMemoryPrototype = WINFUNCTYPE(BOOL, HANDLE, LPVOID, LPCVOID, SIZE_T, POINTER(SIZE_T))
WriteProcessMemoryParams = ((1, 'hProcess'), (1, 'lpBaseAddress'), (1, 'lpBuffer'), (1, 'nSize'), (1, 'lpNumberOfBytesWritten'))



NtWow64WriteVirtualMemory64Prototype = WINFUNCTYPE(NTSTATUS, HANDLE, ULONG64, LPVOID, ULONG64, PULONG64)
NtWow64WriteVirtualMemory64Params = ((1, 'hProcess'), (1, 'lpBaseAddress'), (1, 'lpBuffer'), (1, 'nSize'), (1, 'lpNumberOfBytesWritten'))



GetCurrentProcessPrototype = WINFUNCTYPE(HANDLE)
GetCurrentProcessParams = ()



CreateFileAPrototype = WINFUNCTYPE(HANDLE, LPCSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE)
CreateFileAParams = ((1, 'lpFileName'), (1, 'dwDesiredAccess'), (1, 'dwShareMode'), (1, 'lpSecurityAttributes'), (1, 'dwCreationDisposition'), (1, 'dwFlagsAndAttributes'), (1, 'hTemplateFile'))



CreateFileWPrototype = WINFUNCTYPE(HANDLE, LPCWSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE)
CreateFileWParams = ((1, 'lpFileName'), (1, 'dwDesiredAccess'), (1, 'dwShareMode'), (1, 'lpSecurityAttributes'), (1, 'dwCreationDisposition'), (1, 'dwFlagsAndAttributes'), (1, 'hTemplateFile'))



OpenProcessTokenPrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD, PHANDLE)
OpenProcessTokenParams = ((1, 'ProcessHandle'), (1, 'DesiredAccess'), (1, 'TokenHandle'))



DuplicateTokenPrototype = WINFUNCTYPE(BOOL, HANDLE, SECURITY_IMPERSONATION_LEVEL, PHANDLE)
DuplicateTokenParams = ((1, 'ExistingTokenHandle'), (1, 'ImpersonationLevel'), (1, 'DuplicateTokenHandle'))



DuplicateTokenExPrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD, LPSECURITY_ATTRIBUTES, SECURITY_IMPERSONATION_LEVEL, TOKEN_TYPE, PHANDLE)
DuplicateTokenExParams = ((1, 'hExistingToken'), (1, 'dwDesiredAccess'), (1, 'lpTokenAttributes'), (1, 'ImpersonationLevel'), (1, 'TokenType'), (1, 'phNewToken'))



OpenThreadTokenPrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD, BOOL, PHANDLE)
OpenThreadTokenParams = ((1, 'ThreadHandle'), (1, 'DesiredAccess'), (1, 'OpenAsSelf'), (1, 'TokenHandle'))



SetThreadTokenPrototype = WINFUNCTYPE(BOOL, PHANDLE, HANDLE)
SetThreadTokenParams = ((1, 'Thread'), (1, 'Token'))



LookupPrivilegeValueAPrototype = WINFUNCTYPE(BOOL, LPCSTR, LPCSTR, PLUID)
LookupPrivilegeValueAParams = ((1, 'lpSystemName'), (1, 'lpName'), (1, 'lpLuid'))



LookupPrivilegeValueWPrototype = WINFUNCTYPE(BOOL, LPCWSTR, LPCWSTR, PLUID)
LookupPrivilegeValueWParams = ((1, 'lpSystemName'), (1, 'lpName'), (1, 'lpLuid'))



LookupPrivilegeNameAPrototype = WINFUNCTYPE(BOOL, LPCSTR, PLUID, LPCSTR, LPDWORD)
LookupPrivilegeNameAParams = ((1, 'lpSystemName'), (1, 'lpLuid'), (1, 'lpName'), (1, 'cchName'))



LookupPrivilegeNameWPrototype = WINFUNCTYPE(BOOL, LPCWSTR, PLUID, LPCWSTR, LPDWORD)
LookupPrivilegeNameWParams = ((1, 'lpSystemName'), (1, 'lpLuid'), (1, 'lpName'), (1, 'cchName'))



AdjustTokenPrivilegesPrototype = WINFUNCTYPE(BOOL, HANDLE, BOOL, PTOKEN_PRIVILEGES, DWORD, PTOKEN_PRIVILEGES, PDWORD)
AdjustTokenPrivilegesParams = ((1, 'TokenHandle'), (1, 'DisableAllPrivileges'), (1, 'NewState'), (1, 'BufferLength'), (1, 'PreviousState'), (1, 'ReturnLength'))



FindResourceAPrototype = WINFUNCTYPE(HRSRC, HMODULE, LPCSTR, LPCSTR)
FindResourceAParams = ((1, 'hModule'), (1, 'lpName'), (1, 'lpType'))



FindResourceWPrototype = WINFUNCTYPE(HRSRC, HMODULE, LPCWSTR, LPCWSTR)
FindResourceWParams = ((1, 'hModule'), (1, 'lpName'), (1, 'lpType'))



SizeofResourcePrototype = WINFUNCTYPE(DWORD, HMODULE, HRSRC)
SizeofResourceParams = ((1, 'hModule'), (1, 'hResInfo'))



LoadResourcePrototype = WINFUNCTYPE(HGLOBAL, HMODULE, HRSRC)
LoadResourceParams = ((1, 'hModule'), (1, 'hResInfo'))



LockResourcePrototype = WINFUNCTYPE(LPVOID, HGLOBAL)
LockResourceParams = ((1, 'hResData'),)



FreeResourcePrototype = WINFUNCTYPE(BOOL, HGLOBAL)
FreeResourceParams = ((1, 'hResData'),)



EnumResourceTypesAPrototype = WINFUNCTYPE(BOOL, HMODULE, ENUMRESTYPEPROCA, LONG_PTR)
EnumResourceTypesAParams = ((1, 'hModule'), (1, 'lpEnumFunc'), (1, 'lParam'))



EnumResourceTypesWPrototype = WINFUNCTYPE(BOOL, HMODULE, ENUMRESTYPEPROCW, LONG_PTR)
EnumResourceTypesWParams = ((1, 'hModule'), (1, 'lpEnumFunc'), (1, 'lParam'))



EnumResourceNamesAPrototype = WINFUNCTYPE(BOOL, HMODULE, LPCSTR, ENUMRESNAMEPROCA, LONG_PTR)
EnumResourceNamesAParams = ((1, 'hModule'), (1, 'lpType'), (1, 'lpEnumFunc'), (1, 'lParam'))



EnumResourceNamesWPrototype = WINFUNCTYPE(BOOL, HMODULE, LPCWSTR, ENUMRESNAMEPROCW, LONG_PTR)
EnumResourceNamesWParams = ((1, 'hModule'), (1, 'lpType'), (1, 'lpEnumFunc'), (1, 'lParam'))



GetVersionExAPrototype = WINFUNCTYPE(BOOL, LPOSVERSIONINFOA)
GetVersionExAParams = ((1, 'lpVersionInformation'),)



GetVersionExWPrototype = WINFUNCTYPE(BOOL, LPOSVERSIONINFOW)
GetVersionExWParams = ((1, 'lpVersionInformation'),)



GetVersionPrototype = WINFUNCTYPE(DWORD)
GetVersionParams = ()



GetCurrentThreadPrototype = WINFUNCTYPE(HANDLE)
GetCurrentThreadParams = ()



GetCurrentThreadIdPrototype = WINFUNCTYPE(DWORD)
GetCurrentThreadIdParams = ()



GetCurrentProcessorNumberPrototype = WINFUNCTYPE(DWORD)
GetCurrentProcessorNumberParams = ()



AllocConsolePrototype = WINFUNCTYPE(BOOL)
AllocConsoleParams = ()



FreeConsolePrototype = WINFUNCTYPE(BOOL)
FreeConsoleParams = ()



GetStdHandlePrototype = WINFUNCTYPE(HANDLE, DWORD)
GetStdHandleParams = ((1, 'nStdHandle'),)



SetStdHandlePrototype = WINFUNCTYPE(BOOL, DWORD, HANDLE)
SetStdHandleParams = ((1, 'nStdHandle'), (1, 'hHandle'))



SetThreadAffinityMaskPrototype = WINFUNCTYPE(DWORD, HANDLE, DWORD)
SetThreadAffinityMaskParams = ((1, 'hThread'), (1, 'dwThreadAffinityMask'))



ReadFilePrototype = WINFUNCTYPE(BOOL, HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED)
ReadFileParams = ((1, 'hFile'), (1, 'lpBuffer'), (1, 'nNumberOfBytesToRead'), (1, 'lpNumberOfBytesRead'), (1, 'lpOverlapped'))



WriteFilePrototype = WINFUNCTYPE(BOOL, HANDLE, LPCVOID, DWORD, LPDWORD, LPOVERLAPPED)
WriteFileParams = ((1, 'hFile'), (1, 'lpBuffer'), (1, 'nNumberOfBytesToWrite'), (1, 'lpNumberOfBytesWritten'), (1, 'lpOverlapped'))



AddVectoredContinueHandlerPrototype = WINFUNCTYPE(PVOID, ULONG, PVECTORED_EXCEPTION_HANDLER)
AddVectoredContinueHandlerParams = ((1, 'FirstHandler'), (1, 'VectoredHandler'))



AddVectoredExceptionHandlerPrototype = WINFUNCTYPE(PVOID, ULONG, PVECTORED_EXCEPTION_HANDLER)
AddVectoredExceptionHandlerParams = ((1, 'FirstHandler'), (1, 'VectoredHandler'))



TerminateThreadPrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD)
TerminateThreadParams = ((1, 'hThread'), (1, 'dwExitCode'))



ExitThreadPrototype = WINFUNCTYPE(VOID, DWORD)
ExitThreadParams = ((1, 'dwExitCode'),)



RemoveVectoredExceptionHandlerPrototype = WINFUNCTYPE(ULONG, PVOID)
RemoveVectoredExceptionHandlerParams = ((1, 'Handler'),)



ResumeThreadPrototype = WINFUNCTYPE(DWORD, HANDLE)
ResumeThreadParams = ((1, 'hThread'),)



SuspendThreadPrototype = WINFUNCTYPE(DWORD, HANDLE)
SuspendThreadParams = ((1, 'hThread'),)



WaitForSingleObjectPrototype = WINFUNCTYPE(DWORD, HANDLE, DWORD)
WaitForSingleObjectParams = ((1, 'hHandle'), (1, 'dwMilliseconds'))



GetThreadIdPrototype = WINFUNCTYPE(DWORD, HANDLE)
GetThreadIdParams = ((1, 'Thread'),)



DeviceIoControlPrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD, LPVOID, DWORD, LPVOID, DWORD, LPDWORD, LPOVERLAPPED)
DeviceIoControlParams = ((1, 'hDevice'), (1, 'dwIoControlCode'), (1, 'lpInBuffer'), (1, 'nInBufferSize'), (1, 'lpOutBuffer'), (1, 'nOutBufferSize'), (1, 'lpBytesReturned'), (1, 'lpOverlapped'))



GetTokenInformationPrototype = WINFUNCTYPE(BOOL, HANDLE, TOKEN_INFORMATION_CLASS, LPVOID, DWORD, PDWORD)
GetTokenInformationParams = ((1, 'TokenHandle'), (1, 'TokenInformationClass'), (1, 'TokenInformation'), (1, 'TokenInformationLength'), (1, 'ReturnLength'))



Wow64DisableWow64FsRedirectionPrototype = WINFUNCTYPE(BOOL, POINTER(PVOID))
Wow64DisableWow64FsRedirectionParams = ((1, 'OldValue'),)



Wow64RevertWow64FsRedirectionPrototype = WINFUNCTYPE(BOOL, PVOID)
Wow64RevertWow64FsRedirectionParams = ((1, 'OldValue'),)



Wow64EnableWow64FsRedirectionPrototype = WINFUNCTYPE(BOOLEAN, BOOLEAN)
Wow64EnableWow64FsRedirectionParams = ((1, 'Wow64FsEnableRedirection'),)



Wow64GetThreadContextPrototype = WINFUNCTYPE(BOOL, HANDLE, PWOW64_CONTEXT)
Wow64GetThreadContextParams = ((1, 'hThread'), (1, 'lpContext'))



SetConsoleCtrlHandlerPrototype = WINFUNCTYPE(BOOL, PHANDLER_ROUTINE, BOOL)
SetConsoleCtrlHandlerParams = ((1, 'HandlerRoutine'), (1, 'Add'))



WinVerifyTrustPrototype = WINFUNCTYPE(LONG, HWND, POINTER(GUID), LPVOID)
WinVerifyTrustParams = ((1, 'hwnd'), (1, 'pgActionID'), (1, 'pWVTData'))



GlobalAllocPrototype = WINFUNCTYPE(HGLOBAL, UINT, SIZE_T)
GlobalAllocParams = ((1, 'uFlags'), (1, 'dwBytes'))



GlobalFreePrototype = WINFUNCTYPE(HGLOBAL, HGLOBAL)
GlobalFreeParams = ((1, 'hMem'),)



GlobalUnlockPrototype = WINFUNCTYPE(BOOL, HGLOBAL)
GlobalUnlockParams = ((1, 'hMem'),)



GlobalLockPrototype = WINFUNCTYPE(LPVOID, HGLOBAL)
GlobalLockParams = ((1, 'hMem'),)



OpenClipboardPrototype = WINFUNCTYPE(BOOL, HWND)
OpenClipboardParams = ((1, 'hWndNewOwner'),)



EmptyClipboardPrototype = WINFUNCTYPE(BOOL)
EmptyClipboardParams = ()



CloseClipboardPrototype = WINFUNCTYPE(BOOL)
CloseClipboardParams = ()



SetClipboardDataPrototype = WINFUNCTYPE(HANDLE, UINT, HANDLE)
SetClipboardDataParams = ((1, 'uFormat'), (1, 'hMem'))



GetClipboardDataPrototype = WINFUNCTYPE(HANDLE, UINT)
GetClipboardDataParams = ((1, 'uFormat'),)



EnumClipboardFormatsPrototype = WINFUNCTYPE(UINT, UINT)
EnumClipboardFormatsParams = ((1, 'format'),)



GetClipboardFormatNameAPrototype = WINFUNCTYPE(INT, UINT, LPCSTR, INT)
GetClipboardFormatNameAParams = ((1, 'format'), (1, 'lpszFormatName'), (1, 'cchMaxCount'))



GetClipboardFormatNameWPrototype = WINFUNCTYPE(INT, UINT, LPCWSTR, INT)
GetClipboardFormatNameWParams = ((1, 'format'), (1, 'lpszFormatName'), (1, 'cchMaxCount'))



WinVerifyTrustPrototype = WINFUNCTYPE(LONG, HWND, POINTER(GUID), LPVOID)
WinVerifyTrustParams = ((1, 'hWnd'), (1, 'pgActionID'), (1, 'pWVTData'))



OpenProcessTokenPrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD, PHANDLE)
OpenProcessTokenParams = ((1, 'ProcessHandle'), (1, 'DesiredAccess'), (1, 'TokenHandle'))



OpenThreadTokenPrototype = WINFUNCTYPE(BOOL, HANDLE, DWORD, BOOL, PHANDLE)
OpenThreadTokenParams = ((1, 'ThreadHandle'), (1, 'DesiredAccess'), (1, 'OpenAsSelf'), (1, 'TokenHandle'))



GetTokenInformationPrototype = WINFUNCTYPE(BOOL, HANDLE, TOKEN_INFORMATION_CLASS, LPVOID, DWORD, PDWORD)
GetTokenInformationParams = ((1, 'TokenHandle'), (1, 'TokenInformationClass'), (1, 'TokenInformation'), (1, 'TokenInformationLength'), (1, 'ReturnLength'))



SetTokenInformationPrototype = WINFUNCTYPE(BOOL, HANDLE, TOKEN_INFORMATION_CLASS, LPVOID, DWORD)
SetTokenInformationParams = ((1, 'TokenHandle'), (1, 'TokenInformationClass'), (1, 'TokenInformation'), (1, 'TokenInformationLength'))



CreateWellKnownSidPrototype = WINFUNCTYPE(BOOL, WELL_KNOWN_SID_TYPE, PSID, PSID, POINTER(DWORD))
CreateWellKnownSidParams = ((1, 'WellKnownSidType'), (1, 'DomainSid'), (1, 'pSid'), (1, 'cbSid'))



DebugBreakPrototype = WINFUNCTYPE(VOID)
DebugBreakParams = ()



WaitForDebugEventPrototype = WINFUNCTYPE(BOOL, LPDEBUG_EVENT, DWORD)
WaitForDebugEventParams = ((1, 'lpDebugEvent'), (1, 'dwMilliseconds'))



ContinueDebugEventPrototype = WINFUNCTYPE(BOOL, DWORD, DWORD, DWORD)
ContinueDebugEventParams = ((1, 'dwProcessId'), (1, 'dwThreadId'), (1, 'dwContinueStatus'))



DebugActiveProcessPrototype = WINFUNCTYPE(BOOL, DWORD)
DebugActiveProcessParams = ((1, 'dwProcessId'),)



DebugActiveProcessStopPrototype = WINFUNCTYPE(BOOL, DWORD)
DebugActiveProcessStopParams = ((1, 'dwProcessId'),)



DebugSetProcessKillOnExitPrototype = WINFUNCTYPE(BOOL, BOOL)
DebugSetProcessKillOnExitParams = ((1, 'KillOnExit'),)



DebugBreakProcessPrototype = WINFUNCTYPE(BOOL, HANDLE)
DebugBreakProcessParams = ((1, 'Process'),)



GetProcessIdPrototype = WINFUNCTYPE(DWORD, HANDLE)
GetProcessIdParams = ((1, 'Process'),)



Wow64SetThreadContextPrototype = WINFUNCTYPE(BOOL, HANDLE, POINTER(WOW64_CONTEXT))
Wow64SetThreadContextParams = ((1, 'hThread'), (1, 'lpContext'))



GetMappedFileNameWPrototype = WINFUNCTYPE(DWORD, HANDLE, LPVOID, PVOID, DWORD)
GetMappedFileNameWParams = ((1, 'hProcess'), (1, 'lpv'), (1, 'lpFilename'), (1, 'nSize'))



GetMappedFileNameAPrototype = WINFUNCTYPE(DWORD, HANDLE, LPVOID, PVOID, DWORD)
GetMappedFileNameAParams = ((1, 'hProcess'), (1, 'lpv'), (1, 'lpFilename'), (1, 'nSize'))



RtlInitStringPrototype = WINFUNCTYPE(VOID, PSTRING, LPCSTR)
RtlInitStringParams = ((1, 'DestinationString'), (1, 'SourceString'))



RtlInitUnicodeStringPrototype = WINFUNCTYPE(VOID, PUNICODE_STRING, LPCWSTR)
RtlInitUnicodeStringParams = ((1, 'DestinationString'), (1, 'SourceString'))



RtlAnsiStringToUnicodeStringPrototype = WINFUNCTYPE(NTSTATUS, PUNICODE_STRING, PCANSI_STRING, BOOLEAN)
RtlAnsiStringToUnicodeStringParams = ((1, 'DestinationString'), (1, 'SourceString'), (1, 'AllocateDestinationString'))



RtlDecompressBufferPrototype = WINFUNCTYPE(NTSTATUS, USHORT, PUCHAR, ULONG, PUCHAR, ULONG, PULONG)
RtlDecompressBufferParams = ((1, 'CompressionFormat'), (1, 'UncompressedBuffer'), (1, 'UncompressedBufferSize'), (1, 'CompressedBuffer'), (1, 'CompressedBufferSize'), (1, 'FinalUncompressedSize'))



RtlCompressBufferPrototype = WINFUNCTYPE(NTSTATUS, USHORT, PUCHAR, ULONG, PUCHAR, ULONG, ULONG, PULONG, PVOID)
RtlCompressBufferParams = ((1, 'CompressionFormatAndEngine'), (1, 'UncompressedBuffer'), (1, 'UncompressedBufferSize'), (1, 'CompressedBuffer'), (1, 'CompressedBufferSize'), (1, 'UncompressedChunkSize'), (1, 'FinalCompressedSize'), (1, 'WorkSpace'))



RtlDecompressBufferExPrototype = WINFUNCTYPE(NTSTATUS, USHORT, PUCHAR, ULONG, PUCHAR, ULONG, PULONG, PVOID)
RtlDecompressBufferExParams = ((1, 'CompressionFormat'), (1, 'UncompressedBuffer'), (1, 'UncompressedBufferSize'), (1, 'CompressedBuffer'), (1, 'CompressedBufferSize'), (1, 'FinalUncompressedSize'), (1, 'WorkSpace'))



RtlGetCompressionWorkSpaceSizePrototype = WINFUNCTYPE(NTSTATUS, USHORT, PULONG, PULONG)
RtlGetCompressionWorkSpaceSizeParams = ((1, 'CompressionFormatAndEngine'), (1, 'CompressBufferWorkSpaceSize'), (1, 'CompressFragmentWorkSpaceSize'))



RtlMoveMemoryPrototype = WINFUNCTYPE(VOID, PVOID, PVOID, SIZE_T)
RtlMoveMemoryParams = ((1, 'Destination'), (1, 'Source'), (1, 'Length'))



lstrcmpAPrototype = WINFUNCTYPE(INT, LPCSTR, LPCSTR)
lstrcmpAParams = ((1, 'lpString1'), (1, 'lpString2'))



lstrcmpWPrototype = WINFUNCTYPE(INT, LPCWSTR, LPCWSTR)
lstrcmpWParams = ((1, 'lpString1'), (1, 'lpString2'))



CreateFileMappingAPrototype = WINFUNCTYPE(HANDLE, HANDLE, LPSECURITY_ATTRIBUTES, DWORD, DWORD, DWORD, LPCSTR)
CreateFileMappingAParams = ((1, 'hFile'), (1, 'lpFileMappingAttributes'), (1, 'flProtect'), (1, 'dwMaximumSizeHigh'), (1, 'dwMaximumSizeLow'), (1, 'lpName'))



CreateFileMappingWPrototype = WINFUNCTYPE(HANDLE, HANDLE, LPSECURITY_ATTRIBUTES, DWORD, DWORD, DWORD, LPCWSTR)
CreateFileMappingWParams = ((1, 'hFile'), (1, 'lpFileMappingAttributes'), (1, 'flProtect'), (1, 'dwMaximumSizeHigh'), (1, 'dwMaximumSizeLow'), (1, 'lpName'))



MapViewOfFilePrototype = WINFUNCTYPE(LPVOID, HANDLE, DWORD, DWORD, DWORD, SIZE_T)
MapViewOfFileParams = ((1, 'hFileMappingObject'), (1, 'dwDesiredAccess'), (1, 'dwFileOffsetHigh'), (1, 'dwFileOffsetLow'), (1, 'dwNumberOfBytesToMap'))



GetLogicalDriveStringsAPrototype = WINFUNCTYPE(DWORD, DWORD, LPCSTR)
GetLogicalDriveStringsAParams = ((1, 'nBufferLength'), (1, 'lpBuffer'))



GetLogicalDriveStringsWPrototype = WINFUNCTYPE(DWORD, DWORD, LPWSTR)
GetLogicalDriveStringsWParams = ((1, 'nBufferLength'), (1, 'lpBuffer'))



GetVolumeInformationAPrototype = WINFUNCTYPE(BOOL, LPCSTR, LPSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPSTR, DWORD)
GetVolumeInformationAParams = ((1, 'lpRootPathName'), (1, 'lpVolumeNameBuffer'), (1, 'nVolumeNameSize'), (1, 'lpVolumeSerialNumber'), (1, 'lpMaximumComponentLength'), (1, 'lpFileSystemFlags'), (1, 'lpFileSystemNameBuffer'), (1, 'nFileSystemNameSize'))



GetVolumeInformationWPrototype = WINFUNCTYPE(BOOL, LPWSTR, LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD)
GetVolumeInformationWParams = ((1, 'lpRootPathName'), (1, 'lpVolumeNameBuffer'), (1, 'nVolumeNameSize'), (1, 'lpVolumeSerialNumber'), (1, 'lpMaximumComponentLength'), (1, 'lpFileSystemFlags'), (1, 'lpFileSystemNameBuffer'), (1, 'nFileSystemNameSize'))



GetVolumeNameForVolumeMountPointAPrototype = WINFUNCTYPE(BOOL, LPCSTR, LPCSTR, DWORD)
GetVolumeNameForVolumeMountPointAParams = ((1, 'lpszVolumeMountPoint'), (1, 'lpszVolumeName'), (1, 'cchBufferLength'))



GetVolumeNameForVolumeMountPointWPrototype = WINFUNCTYPE(BOOL, LPWSTR, LPWSTR, DWORD)
GetVolumeNameForVolumeMountPointWParams = ((1, 'lpszVolumeMountPoint'), (1, 'lpszVolumeName'), (1, 'cchBufferLength'))



GetDriveTypeAPrototype = WINFUNCTYPE(UINT, LPCSTR)
GetDriveTypeAParams = ((1, 'lpRootPathName'),)



GetDriveTypeWPrototype = WINFUNCTYPE(UINT, LPWSTR)
GetDriveTypeWParams = ((1, 'lpRootPathName'),)



QueryDosDeviceAPrototype = WINFUNCTYPE(DWORD, LPCSTR, LPCSTR, DWORD)
QueryDosDeviceAParams = ((1, 'lpDeviceName'), (1, 'lpTargetPath'), (1, 'ucchMax'))



QueryDosDeviceWPrototype = WINFUNCTYPE(DWORD, LPWSTR, LPWSTR, DWORD)
QueryDosDeviceWParams = ((1, 'lpDeviceName'), (1, 'lpTargetPath'), (1, 'ucchMax'))



FindFirstVolumeAPrototype = WINFUNCTYPE(HANDLE, LPCSTR, DWORD)
FindFirstVolumeAParams = ((1, 'lpszVolumeName'), (1, 'cchBufferLength'))



FindFirstVolumeWPrototype = WINFUNCTYPE(HANDLE, LPWSTR, DWORD)
FindFirstVolumeWParams = ((1, 'lpszVolumeName'), (1, 'cchBufferLength'))



FindNextVolumeAPrototype = WINFUNCTYPE(BOOL, HANDLE, LPCSTR, DWORD)
FindNextVolumeAParams = ((1, 'hFindVolume'), (1, 'lpszVolumeName'), (1, 'cchBufferLength'))



FindNextVolumeWPrototype = WINFUNCTYPE(BOOL, HANDLE, LPWSTR, DWORD)
FindNextVolumeWParams = ((1, 'hFindVolume'), (1, 'lpszVolumeName'), (1, 'cchBufferLength'))



DuplicateHandlePrototype = WINFUNCTYPE(BOOL, HANDLE, HANDLE, HANDLE, LPHANDLE, DWORD, BOOL, DWORD)
DuplicateHandleParams = ((1, 'hSourceProcessHandle'), (1, 'hSourceHandle'), (1, 'hTargetProcessHandle'), (1, 'lpTargetHandle'), (1, 'dwDesiredAccess'), (1, 'bInheritHandle'), (1, 'dwOptions'))



ZwDuplicateObjectPrototype = WINFUNCTYPE(NTSTATUS, HANDLE, HANDLE, HANDLE, PHANDLE, ACCESS_MASK, ULONG, ULONG)
ZwDuplicateObjectParams = ((1, 'SourceProcessHandle'), (1, 'SourceHandle'), (1, 'TargetProcessHandle'), (1, 'TargetHandle'), (1, 'DesiredAccess'), (1, 'HandleAttributes'), (1, 'Options'))



GetModuleBaseNameAPrototype = WINFUNCTYPE(DWORD, HANDLE, HMODULE, LPCSTR, DWORD)
GetModuleBaseNameAParams = ((1, 'hProcess'), (1, 'hModule'), (1, 'lpBaseName'), (1, 'nSize'))



GetModuleBaseNameWPrototype = WINFUNCTYPE(DWORD, HANDLE, HMODULE, LPWSTR, DWORD)
GetModuleBaseNameWParams = ((1, 'hProcess'), (1, 'hModule'), (1, 'lpBaseName'), (1, 'nSize'))



GetProcessImageFileNameAPrototype = WINFUNCTYPE(DWORD, HANDLE, LPCSTR, DWORD)
GetProcessImageFileNameAParams = ((1, 'hProcess'), (1, 'lpImageFileName'), (1, 'nSize'))



GetProcessImageFileNameWPrototype = WINFUNCTYPE(DWORD, HANDLE, LPWSTR, DWORD)
GetProcessImageFileNameWParams = ((1, 'hProcess'), (1, 'lpImageFileName'), (1, 'nSize'))



GetSystemMetricsPrototype = WINFUNCTYPE(INT, INT)
GetSystemMetricsParams = ((1, 'nIndex'),)



GetInterfaceInfoPrototype = WINFUNCTYPE(DWORD, PIP_INTERFACE_INFO, PULONG)
GetInterfaceInfoParams = ((1, 'pIfTable'), (1, 'dwOutBufLen'))



GetIfTablePrototype = WINFUNCTYPE(DWORD, PMIB_IFTABLE, PULONG, BOOL)
GetIfTableParams = ((1, 'pIfTable'), (1, 'pdwSize'), (1, 'bOrder'))



GetIpAddrTablePrototype = WINFUNCTYPE(DWORD, PMIB_IPADDRTABLE, PULONG, BOOL)
GetIpAddrTableParams = ((1, 'pIpAddrTable'), (1, 'pdwSize'), (1, 'bOrder'))



GetProcessTimesPrototype = WINFUNCTYPE(BOOL, HANDLE, LPFILETIME, LPFILETIME, LPFILETIME, LPFILETIME)
GetProcessTimesParams = ((1, 'hProcess'), (1, 'lpCreationTime'), (1, 'lpExitTime'), (1, 'lpKernelTime'), (1, 'lpUserTime'))



GetShortPathNameAPrototype = WINFUNCTYPE(DWORD, LPCSTR, LPCSTR, DWORD)
GetShortPathNameAParams = ((1, 'lpszLongPath'), (1, 'lpszShortPath'), (1, 'cchBuffer'))



GetShortPathNameWPrototype = WINFUNCTYPE(DWORD, LPWSTR, LPWSTR, DWORD)
GetShortPathNameWParams = ((1, 'lpszLongPath'), (1, 'lpszShortPath'), (1, 'cchBuffer'))



GetLongPathNameAPrototype = WINFUNCTYPE(DWORD, LPCSTR, LPCSTR, DWORD)
GetLongPathNameAParams = ((1, 'lpszShortPath'), (1, 'lpszLongPath'), (1, 'cchBuffer'))



GetLongPathNameWPrototype = WINFUNCTYPE(DWORD, LPWSTR, LPWSTR, DWORD)
GetLongPathNameWParams = ((1, 'lpszShortPath'), (1, 'lpszLongPath'), (1, 'cchBuffer'))



GetProcessDEPPolicyPrototype = WINFUNCTYPE(BOOL, HANDLE, LPDWORD, PBOOL)
GetProcessDEPPolicyParams = ((1, 'hProcess'), (1, 'lpFlags'), (1, 'lpPermanent'))



ConvertStringSidToSidAPrototype = WINFUNCTYPE(BOOL, LPCSTR, POINTER(PSID))
ConvertStringSidToSidAParams = ((1, 'StringSid'), (1, 'Sid'))



ConvertStringSidToSidWPrototype = WINFUNCTYPE(BOOL, LPWSTR, POINTER(PSID))
ConvertStringSidToSidWParams = ((1, 'StringSid'), (1, 'Sid'))



ConvertSidToStringSidAPrototype = WINFUNCTYPE(BOOL, PSID, POINTER(LPCSTR))
ConvertSidToStringSidAParams = ((1, 'Sid'), (1, 'StringSid'))



ConvertSidToStringSidWPrototype = WINFUNCTYPE(BOOL, PSID, POINTER(LPWSTR))
ConvertSidToStringSidWParams = ((1, 'Sid'), (1, 'StringSid'))



LocalFreePrototype = WINFUNCTYPE(HLOCAL, HLOCAL)
LocalFreeParams = ((1, 'hMem'),)



InitializeProcThreadAttributeListPrototype = WINFUNCTYPE(BOOL, LPPROC_THREAD_ATTRIBUTE_LIST, DWORD, DWORD, PSIZE_T)
InitializeProcThreadAttributeListParams = ((1, 'lpAttributeList'), (1, 'dwAttributeCount'), (1, 'dwFlags'), (1, 'lpSize'))



UpdateProcThreadAttributePrototype = WINFUNCTYPE(BOOL, LPPROC_THREAD_ATTRIBUTE_LIST, DWORD, DWORD_PTR, PVOID, SIZE_T, PVOID, PSIZE_T)
UpdateProcThreadAttributeParams = ((1, 'lpAttributeList'), (1, 'dwFlags'), (1, 'Attribute'), (1, 'lpValue'), (1, 'cbSize'), (1, 'lpPreviousValue'), (1, 'lpReturnSize'))



DeleteProcThreadAttributeListPrototype = WINFUNCTYPE(VOID, LPPROC_THREAD_ATTRIBUTE_LIST)
DeleteProcThreadAttributeListParams = ((1, 'lpAttributeList'),)



MessageBoxAPrototype = WINFUNCTYPE(INT, HWND, LPCSTR, LPCSTR, UINT)
MessageBoxAParams = ((1, 'hWnd'), (1, 'lpText'), (1, 'lpCaption'), (1, 'uType'))



MessageBoxWPrototype = WINFUNCTYPE(INT, HWND, LPWSTR, LPWSTR, UINT)
MessageBoxWParams = ((1, 'hWnd'), (1, 'lpText'), (1, 'lpCaption'), (1, 'uType'))



GetWindowsDirectoryAPrototype = WINFUNCTYPE(UINT, LPCSTR, UINT)
GetWindowsDirectoryAParams = ((1, 'lpBuffer'), (1, 'uSize'))



GetWindowsDirectoryWPrototype = WINFUNCTYPE(UINT, LPWSTR, UINT)
GetWindowsDirectoryWParams = ((1, 'lpBuffer'), (1, 'uSize'))



RtlGetUnloadEventTraceExPrototype = WINFUNCTYPE(VOID, POINTER(PULONG), POINTER(PULONG), POINTER(PVOID))
RtlGetUnloadEventTraceExParams = ((1, 'ElementSize'), (1, 'ElementCount'), (1, 'EventTrace'))



RtlDosPathNameToNtPathName_UPrototype = WINFUNCTYPE(BOOLEAN, PCWSTR, PUNICODE_STRING, POINTER(PCWSTR), PRTL_RELATIVE_NAME_U)
RtlDosPathNameToNtPathName_UParams = ((1, 'DosName'), (1, 'NtName'), (1, 'PartName'), (1, 'RelativeName'))



ApiSetResolveToHostPrototype = WINFUNCTYPE(NTSTATUS, PVOID, PUNICODE_STRING, PUNICODE_STRING, PBOOLEAN, PUNICODE_STRING)
ApiSetResolveToHostParams = ((1, 'Schema'), (1, 'FileNameIn'), (1, 'ParentName'), (1, 'Resolved'), (1, 'HostBinary'))



SleepPrototype = WINFUNCTYPE(VOID, DWORD)
SleepParams = ((1, 'dwMilliseconds'),)



SleepExPrototype = WINFUNCTYPE(DWORD, DWORD, BOOL)
SleepExParams = ((1, 'dwMilliseconds'), (1, 'bAlertable'))



GetProcessMitigationPolicyPrototype = WINFUNCTYPE(BOOL, HANDLE, PROCESS_MITIGATION_POLICY, PVOID, SIZE_T)
GetProcessMitigationPolicyParams = ((1, 'hProcess'), (1, 'MitigationPolicy'), (1, 'lpBuffer'), (1, 'dwLength'))



SetProcessMitigationPolicyPrototype = WINFUNCTYPE(BOOL, PROCESS_MITIGATION_POLICY, PVOID, SIZE_T)
SetProcessMitigationPolicyParams = ((1, 'MitigationPolicy'), (1, 'lpBuffer'), (1, 'dwLength'))



GetProductInfoPrototype = WINFUNCTYPE(BOOL, DWORD, DWORD, DWORD, DWORD, PDWORD)
GetProductInfoParams = ((1, 'dwOSMajorVersion'), (1, 'dwOSMinorVersion'), (1, 'dwSpMajorVersion'), (1, 'dwSpMinorVersion'), (1, 'pdwReturnedProductType'))



GetProcessMemoryInfoPrototype = WINFUNCTYPE(BOOL, HANDLE, PPROCESS_MEMORY_COUNTERS, DWORD)
GetProcessMemoryInfoParams = ((1, 'Process'), (1, 'ppsmemCounters'), (1, 'cb'))



GetModuleHandleAPrototype = WINFUNCTYPE(HMODULE, LPCSTR)
GetModuleHandleAParams = ((1, 'lpModuleName'),)



GetModuleHandleWPrototype = WINFUNCTYPE(HMODULE, LPWSTR)
GetModuleHandleWParams = ((1, 'lpModuleName'),)



RtlEqualUnicodeStringPrototype = WINFUNCTYPE(BOOLEAN, PUNICODE_STRING, PUNICODE_STRING, BOOLEAN)
RtlEqualUnicodeStringParams = ((1, 'String1'), (1, 'String2'), (1, 'CaseInSensitive'))



GetFirmwareEnvironmentVariableAPrototype = WINFUNCTYPE(DWORD, LPCSTR, LPCSTR, PVOID, DWORD)
GetFirmwareEnvironmentVariableAParams = ((1, 'lpName'), (1, 'lpGuid'), (1, 'pBuffer'), (1, 'nSize'))



GetFirmwareEnvironmentVariableWPrototype = WINFUNCTYPE(DWORD, LPCWSTR, LPCWSTR, PVOID, DWORD)
GetFirmwareEnvironmentVariableWParams = ((1, 'lpName'), (1, 'lpGuid'), (1, 'pBuffer'), (1, 'nSize'))



GetFirmwareEnvironmentVariableExAPrototype = WINFUNCTYPE(DWORD, LPCSTR, LPCSTR, PVOID, DWORD, PDWORD)
GetFirmwareEnvironmentVariableExAParams = ((1, 'lpName'), (1, 'lpGuid'), (1, 'pBuffer'), (1, 'nSize'), (1, 'pdwAttribubutes'))



GetFirmwareEnvironmentVariableExWPrototype = WINFUNCTYPE(DWORD, LPCWSTR, LPCWSTR, PVOID, DWORD, PDWORD)
GetFirmwareEnvironmentVariableExWParams = ((1, 'lpName'), (1, 'lpGuid'), (1, 'pBuffer'), (1, 'nSize'), (1, 'pdwAttribubutes'))



IsDebuggerPresentPrototype = WINFUNCTYPE(BOOL)
IsDebuggerPresentParams = ()



WSAStartupPrototype = WINFUNCTYPE(INT, WORD, LPWSADATA)
WSAStartupParams = ((1, 'wVersionRequested'), (1, 'lpWSAData'))



WSACleanupPrototype = WINFUNCTYPE(INT)
WSACleanupParams = ()



WSAGetLastErrorPrototype = WINFUNCTYPE(INT)
WSAGetLastErrorParams = ()



getaddrinfoPrototype = WINFUNCTYPE(INT, PCSTR, PCSTR, POINTER(ADDRINFOA), POINTER(PADDRINFOA))
getaddrinfoParams = ((1, 'pNodeName'), (1, 'pServiceName'), (1, 'pHints'), (1, 'ppResult'))



GetAddrInfoWPrototype = WINFUNCTYPE(INT, PCWSTR, PCWSTR, POINTER(ADDRINFOW), POINTER(PADDRINFOW))
GetAddrInfoWParams = ((1, 'pNodeName'), (1, 'pServiceName'), (1, 'pHints'), (1, 'ppResult'))



WSASocketAPrototype = WINFUNCTYPE(SOCKET, INT, INT, INT, LPWSAPROTOCOL_INFOA, GROUP, DWORD)
WSASocketAParams = ((1, 'af'), (1, 'type'), (1, 'protocol'), (1, 'lpProtocolInfo'), (1, 'g'), (1, 'dwFlags'))



WSASocketWPrototype = WINFUNCTYPE(SOCKET, INT, INT, INT, LPWSAPROTOCOL_INFOW, GROUP, DWORD)
WSASocketWParams = ((1, 'af'), (1, 'type'), (1, 'protocol'), (1, 'lpProtocolInfo'), (1, 'g'), (1, 'dwFlags'))



socketPrototype = WINFUNCTYPE(SOCKET, INT, INT, INT)
socketParams = ((1, 'af'), (1, 'type'), (1, 'protocol'))



connectPrototype = WINFUNCTYPE(INT, SOCKET, POINTER(sockaddr), INT)
connectParams = ((1, 's'), (1, 'name'), (1, 'namelen'))



sendPrototype = WINFUNCTYPE(INT, SOCKET, POINTER(CHAR), INT, INT)
sendParams = ((1, 's'), (1, 'buf'), (1, 'len'), (1, 'flags'))



recvPrototype = WINFUNCTYPE(INT, SOCKET, POINTER(CHAR), INT, INT)
recvParams = ((1, 's'), (1, 'buf'), (1, 'len'), (1, 'flags'))



shutdownPrototype = WINFUNCTYPE(INT, SOCKET, INT)
shutdownParams = ((1, 's'), (1, 'how'))



closesocketPrototype = WINFUNCTYPE(INT, SOCKET)
closesocketParams = ((1, 's'),)

