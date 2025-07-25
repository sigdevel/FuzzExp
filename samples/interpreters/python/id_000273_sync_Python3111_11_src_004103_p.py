



"License");






"AS IS" BASIS,




import inspect
import warnings
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import tensorflow as tf
from tensorflow.compiler.tf2xla.python.xla import dynamic_update_slice

from .generation_tf_logits_process import (
    TFForcedBOSTokenLogitsProcessor,
    TFForcedEOSTokenLogitsProcessor,
    TFForceTokensLogitsProcessor,
    TFLogitsProcessorList,
    TFMinLengthLogitsProcessor,
    TFNoBadWordsLogitsProcessor,
    TFNoRepeatNGramLogitsProcessor,
    TFRepetitionPenaltyLogitsProcessor,
    TFSuppressTokensAtBeginLogitsProcessor,
    TFSuppressTokensLogitsProcessor,
    TFTemperatureLogitsWarper,
    TFTopKLogitsWarper,
    TFTopPLogitsWarper,
)
from .models.auto import (
    TF_MODEL_FOR_CAUSAL_LM_MAPPING,
    TF_MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING,
    TF_MODEL_FOR_SPEECH_SEQ_2_SEQ_MAPPING,
    TF_MODEL_FOR_VISION_2_SEQ_MAPPING,
)
from .tf_utils import shape_list, stable_softmax
from .utils import ModelOutput, logging


logger = logging.get_logger(__name__)


@dataclass
class TFGreedySearchDecoderOnlyOutput(ModelOutput):
    """
    Base class for outputs of decoder-only generation models using greedy search.


    Args:
        sequences (`tf.Tensor` of shape `(batch_size, sequence_length)`):
            The generated sequences. The second dimension (sequence_length) is either equal to `max_length` or shorter
            if all batches finished early due to the `eos_token_id`.
        scores (`tuple(tf.Tensor)` *optional*, returned when `output_scores=True` is passed or when `config.output_scores=True`):
            Processed prediction scores of the language modeling head (scores for each vocabulary token before SoftMax)
            at each generation step. Tuple of `tf.Tensor` with up to `max_new_tokens` elements (one element for each
            generated token), with each tensor of shape `(batch_size, config.vocab_size)`.
        attentions (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size, num_heads, generated_length, sequence_length)`.
        hidden_states (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size, generated_length, hidden_size)`.
    """

    sequences: tf.Tensor = None
    scores: Optional[Tuple[tf.Tensor]] = None
    attentions: Optional[Tuple[Tuple[tf.Tensor]]] = None
    hidden_states: Optional[Tuple[Tuple[tf.Tensor]]] = None


@dataclass
class TFGreedySearchEncoderDecoderOutput(ModelOutput):
    """
    Base class for outputs of encoder-decoder generation models using greedy search. Hidden states and attention
    weights of the decoder (respectively the encoder) can be accessed via the encoder_attentions and the
    encoder_hidden_states attributes (respectively the decoder_attentions and the decoder_hidden_states attributes)


    Args:
        sequences (`tf.Tensor` of shape `(batch_size, sequence_length)`):
            The generated sequences. The second dimension (sequence_length) is either equal to `max_length` or shorter
            if all batches finished early due to the `eos_token_id`.
        scores (`tuple(tf.Tensor)` *optional*, returned when `output_scores=True` is passed or when `config.output_scores=True`):
            Processed prediction scores of the language modeling head (scores for each vocabulary token before SoftMax)
            at each generation step. Tuple of `tf.Tensor` with up to `max_new_tokens` elements (one element for each
            generated token), with each tensor of shape `(batch_size, config.vocab_size)`.
        encoder_attentions (`tuple(tf.Tensor)`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple of `tf.Tensor` (one for each layer of the decoder) of shape `(batch_size, num_heads, sequence_length,
            sequence_length)`.
        encoder_hidden_states (`tuple(tf.Tensor)`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`):
            Tuple of `tf.Tensor` (one for the output of the embeddings + one for the output of each layer) of shape
            `(batch_size, sequence_length, hidden_size)`.
        decoder_attentions (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size, num_heads, generated_length, sequence_length)`.
        cross_attentions (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size, num_heads, generated_length, sequence_length)`.
        decoder_hidden_states (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size, generated_length, hidden_size)`.
    """

    sequences: tf.Tensor = None
    scores: Optional[Tuple[tf.Tensor]] = None
    encoder_attentions: Optional[Tuple[tf.Tensor]] = None
    encoder_hidden_states: Optional[Tuple[tf.Tensor]] = None
    decoder_attentions: Optional[Tuple[Tuple[tf.Tensor]]] = None
    cross_attentions: Optional[Tuple[Tuple[tf.Tensor]]] = None
    decoder_hidden_states: Optional[Tuple[Tuple[tf.Tensor]]] = None


@dataclass
class TFSampleDecoderOnlyOutput(ModelOutput):
    """
    Base class for outputs of decoder-only generation models using sampling.


    Args:
        sequences (`tf.Tensor` of shape `(batch_size*num_return_sequences, sequence_length)`):
            The generated sequences. The second dimension (sequence_length) is either equal to `max_length` or shorter
            if all batches finished early due to the `eos_token_id`.
        scores (`tuple(tf.Tensor)` *optional*, returned when `output_scores=True` is passed or when `config.output_scores=True`):
            Processed prediction scores of the language modeling head (scores for each vocabulary token before SoftMax)
            at each generation step. Tuple of `tf.Tensor` with up to `max_new_tokens` elements (one element for each
            generated token), with each tensor of shape `(batch_size*num_return_sequences, config.vocab_size)`.
        attentions (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(num_return_sequences*batch_size, num_heads, generated_length, sequence_length)`.
        hidden_states (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(num_return_sequences*batch_size, generated_length, hidden_size)`.
    """

    sequences: tf.Tensor = None
    scores: Optional[Tuple[tf.Tensor]] = None
    attentions: Optional[Tuple[Tuple[tf.Tensor]]] = None
    hidden_states: Optional[Tuple[Tuple[tf.Tensor]]] = None


@dataclass
class TFSampleEncoderDecoderOutput(ModelOutput):
    """
    Base class for outputs of encoder-decoder generation models using sampling. Hidden states and attention weights of
    the decoder (respectively the encoder) can be accessed via the encoder_attentions and the encoder_hidden_states
    attributes (respectively the decoder_attentions and the decoder_hidden_states attributes)


    Args:
        sequences (`tf.Tensor` of shape `(batch_size*num_return_sequences, sequence_length)`):
            The generated sequences. The second dimension (sequence_length) is either equal to `max_length` or shorter
            if all batches finished early due to the `eos_token_id`.
        scores (`tuple(tf.Tensor)` *optional*, returned when `output_scores=True` is passed or when `config.output_scores=True`):
            Processed prediction scores of the language modeling head (scores for each vocabulary token before SoftMax)
            at each generation step. Tuple of `tf.Tensor` with up to `max_new_tokens` elements (one element for each
            generated token), with each tensor of shape `(batch_size*num_return_sequences, config.vocab_size)`.
        encoder_attentions (`tuple(tf.Tensor)`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple of `tf.Tensor` (one for each layer of the decoder) of shape `(batch_size*num_return_sequences,
            num_heads, sequence_length, sequence_length)`.
        encoder_hidden_states (`tuple(tf.Tensor)`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`):
            Tuple of `tf.Tensor` (one for the output of the embeddings + one for the output of each layer) of shape
            `(batch_size*num_return_sequences, sequence_length, hidden_size)`.
        decoder_attentions (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size*num_return_sequences, num_heads, generated_length, sequence_length)`.
        cross_attentions (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size, num_heads, generated_length, sequence_length)`.
        decoder_hidden_states (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size*num_return_sequences, generated_length, hidden_size)`.
    """

    sequences: tf.Tensor = None
    scores: Optional[Tuple[tf.Tensor]] = None
    encoder_attentions: Optional[Tuple[tf.Tensor]] = None
    encoder_hidden_states: Optional[Tuple[tf.Tensor]] = None
    decoder_attentions: Optional[Tuple[Tuple[tf.Tensor]]] = None
    cross_attentions: Optional[Tuple[Tuple[tf.Tensor]]] = None
    decoder_hidden_states: Optional[Tuple[Tuple[tf.Tensor]]] = None


@dataclass
class TFBeamSearchDecoderOnlyOutput(ModelOutput):
    """
    Base class for outputs of decoder-only generation models using beam search.

    Args:
        sequences (`tf.Tensor` of shape `(batch_size*num_return_sequences, sequence_length)`):
            The generated sequences. The second dimension (sequence_length) is either equal to `max_length` or shorter
            if all batches finished early due to the `eos_token_id`.
        sequences_scores (`tf.Tensor` of shape `(batch_size*num_return_sequences)`, *optional*, returned when `output_scores=True` is passed or when `config.output_scores=True`):
            Final beam scores of the generated `sequences`.
        scores (`tuple(tf.Tensor)` *optional*, returned when `output_scores=True` is passed or when `config.output_scores=True`):
            Processed beam scores for each vocabulary token at each generation step. Beam scores consisting of log
            softmax scores for each vocabulary token and sum of log softmax of previously generated tokens in this
            beam. Tuple of `tf.Tensor` with up to `max_new_tokens` elements (one element for each generated token),
            with each tensor of shape `(batch_size*num_beams*num_return_sequences, config.vocab_size)`.
        attentions (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size*num_beams, num_heads, generated_length, sequence_length)`.
        hidden_states (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size*num_beams*num_return_sequences, generated_length, hidden_size)`.
    """

    sequences: tf.Tensor = None
    sequences_scores: Optional[tf.Tensor] = None
    scores: Optional[Tuple[tf.Tensor]] = None
    attentions: Optional[Tuple[Tuple[tf.Tensor]]] = None
    hidden_states: Optional[Tuple[Tuple[tf.Tensor]]] = None


@dataclass
class TFBeamSearchEncoderDecoderOutput(ModelOutput):
    """
    Base class for outputs of encoder-decoder generation models using beam search. Hidden states and attention weights
    of the decoder (respectively the encoder) can be accessed via the encoder_attentions and the encoder_hidden_states
    attributes (respectively the decoder_attentions and the decoder_hidden_states attributes)

    Args:
        sequences (`tf.Tensor` of shape `(batch_size*num_return_sequences, sequence_length)`):
            The generated sequences. The second dimension (sequence_length) is either equal to `max_length` or shorter
            if all batches finished early due to the `eos_token_id`.
        sequences_scores (`tf.Tensor` of shape `(batch_size*num_return_sequences)`, *optional*, returned when `output_scores=True` is passed or when `config.output_scores=True`):
            Final beam scores of the generated `sequences`.
        scores (`tuple(tf.Tensor)` *optional*, returned when `output_scores=True` is passed or when `config.output_scores=True`):
            Processed beam scores for each vocabulary token at each generation step. Beam scores consisting of log
            softmax scores for each vocabulary token and sum of log softmax of previously generated tokens in this
            beam. `Tuple of `tf.Tensor` with up to `max_new_tokens` elements (one element for each generated token),
            with each tensor of shape `(batch_size*num_beams, config.vocab_size)`.
        attentions (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
        encoder_attentions (`tuple(tf.Tensor)`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple of `tf.Tensor` (one for each layer of the decoder) of shape `(batch_size, num_heads, sequence_length,
            sequence_length)`.
        encoder_hidden_states (`tuple(tf.Tensor)`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`):
            Tuple of `tf.Tensor` (one for the output of the embeddings + one for the output of each layer) of shape
            `(batch_size*num_beams*num_return_sequences, sequence_length, hidden_size)`.
        decoder_attentions (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size*num_beams*num_return_sequences, num_heads, generated_length,
            sequence_length)`.
        cross_attentions (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size, num_heads, generated_length, sequence_length)`.
        decoder_hidden_states (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size*num_beams*num_return_sequences, generated_length, hidden_size)`.
    """

    sequences: tf.Tensor = None
    sequences_scores: Optional[tf.Tensor] = None
    scores: Optional[Tuple[tf.Tensor]] = None
    encoder_attentions: Optional[Tuple[tf.Tensor]] = None
    encoder_hidden_states: Optional[Tuple[tf.Tensor]] = None
    decoder_attentions: Optional[Tuple[Tuple[tf.Tensor]]] = None
    cross_attentions: Optional[Tuple[Tuple[tf.Tensor]]] = None
    decoder_hidden_states: Optional[Tuple[Tuple[tf.Tensor]]] = None


@dataclass
class TFBeamSampleDecoderOnlyOutput(ModelOutput):
    """
    Base class for outputs of decoder-only generation models using beam sample.

    Args:
        sequences (`tf.Tensor` of shape `(batch_size*num_return_sequences, sequence_length)`):
            The generated sequences. The second dimension (sequence_length) is either equal to `max_length` or shorter
            if all batches finished early due to the `eos_token_id`.
        sequences_scores (`tf.Tensor` of shape `(batch_size * num_return_sequence)`, *optional*, returned when `output_scores=True` is passed or when `config.output_scores=True`):
            Final beam scores of the generated `sequences`.
        scores (`tuple(tf.Tensor)` *optional*, returned when `output_scores=True` is passed or when `config.output_scores=True`):
            Processed beam scores for each vocabulary token at each generation step. Beam scores consisting of log
            softmax scores for each vocabulary token and sum of log softmax of previously generated tokens in this
            beam. Tuple of `tf.Tensor` with up to `max_new_tokens` elements (one element for each generated token),
            with each tensor of shape `(batch_size*num_beams*num_return_sequences, config.vocab_size)`.
        attentions (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size*num_beams, num_heads, generated_length, sequence_length)`.
        hidden_states (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size*num_beams, generated_length, hidden_size)`.
    """

    sequences: tf.Tensor = None
    sequences_scores: Optional[tf.Tensor] = None
    scores: Optional[Tuple[tf.Tensor]] = None
    attentions: Optional[Tuple[Tuple[tf.Tensor]]] = None
    hidden_states: Optional[Tuple[Tuple[tf.Tensor]]] = None


@dataclass
class TFBeamSampleEncoderDecoderOutput(ModelOutput):
    """
    Base class for outputs of encoder-decoder generation models using beam sampling. Hidden states and attention
    weights of the decoder (respectively the encoder) can be accessed via the encoder_attentions and the
    encoder_hidden_states attributes (respectively the decoder_attentions and the decoder_hidden_states attributes)

    Args:
        sequences (`tf.Tensor` of shape `(batch_size*num_beams, sequence_length)`):
            The generated sequences. The second dimension (sequence_length) is either equal to `max_length` or shorter
            if all batches finished early due to the `eos_token_id`.
        sequences_scores (`tf.Tensor` of shape `(batch_size * num_return_sequence)`, *optional*, returned when `output_scores=True` is passed or when `config.output_scores=True`):
            Final beam scores of the generated `sequences`.
        scores (`tuple(tf.Tensor)` *optional*, returned when `output_scores=True` is passed or when `config.output_scores=True`):
            Processed beam scores for each vocabulary token at each generation step. Beam scores consisting of log
            softmax scores for each vocabulary token and sum of log softmax of previously generated tokens in this
            beam. Tuple of `tf.Tensor` with up to `max_new_tokens` elements (one element for each generated token),
            with each tensor of shape `(batch_size*num_beams, config.vocab_size)`.
        encoder_attentions (`tuple(tf.Tensor)`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple of `tf.Tensor` (one for each layer of the decoder) of shape `(batch_size, num_heads, sequence_length,
            sequence_length)`.
        encoder_hidden_states (`tuple(tf.Tensor)`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`):
            Tuple of `tf.Tensor` (one for the output of the embeddings + one for the output of each layer) of shape
            `(batch_size*num_beams, sequence_length, hidden_size)`.
        decoder_attentions (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size*num_beams, num_heads, generated_length, sequence_length)`.
        cross_attentions (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_attentions=True` is passed or `config.output_attentions=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size, num_heads, generated_length, sequence_length)`.
        decoder_hidden_states (`tuple(tuple(tf.Tensor))`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`):
            Tuple (one element for each generated token) of tuples (one element for each layer of the decoder) of
            `tf.Tensor` of shape `(batch_size*num_beams, generated_length, hidden_size)`.
    """

    sequences: tf.Tensor = None
    sequences_scores: Optional[tf.Tensor] = None
    scores: Optional[Tuple[tf.Tensor]] = None
    encoder_attentions: Optional[Tuple[tf.Tensor]] = None
    encoder_hidden_states: Optional[Tuple[tf.Tensor]] = None
    decoder_attentions: Optional[Tuple[Tuple[tf.Tensor]]] = None
    cross_attentions: Optional[Tuple[Tuple[tf.Tensor]]] = None
    decoder_hidden_states: Optional[Tuple[Tuple[tf.Tensor]]] = None


TFGreedySearchOutput = Union[TFGreedySearchEncoderDecoderOutput, TFGreedySearchDecoderOnlyOutput]
TFSampleOutput = Union[TFSampleEncoderDecoderOutput, TFSampleDecoderOnlyOutput]
TFBeamSearchOutput = Union[TFBeamSearchEncoderDecoderOutput, TFBeamSearchDecoderOnlyOutput]
TFBeamSampleOutput = Union[TFBeamSampleEncoderDecoderOutput, TFBeamSampleDecoderOnlyOutput]


class TFGenerationMixin:
    """
    A class containing all of the functions supporting generation, to be used as a mixin in [`TFPreTrainedModel`].
    """

    _seed_generator = None

    @property
    def seed_generator(self):
        warnings.warn("`seed_generator` is deprecated and will be removed in a future version.", UserWarning)
        if self._seed_generator is None:
            self._seed_generator = tf.random.Generator.from_non_deterministic_state()
        return self._seed_generator

    supports_xla_generation = True

    def _use_cache(self, outputs, use_cache):
        """During generation, decide whether to pass the `past` variable to the next forward pass."""
        use_cache = getattr(self.config, "use_cache", False)
        if len(outputs) <= 1 or use_cache is False:
            return False
        if hasattr(self.config, "mem_len") and self.config.mem_len == 0:
            return False
        return True

    def generate(
        self,
        input_ids=None,
        max_length=None,
        max_new_tokens=None,
        min_length=None,
        do_sample=None,
        early_stopping=None,
        num_beams=None,
        temperature=None,
        top_k=None,
        top_p=None,
        repetition_penalty=None,
        bad_words_ids=None,
        bos_token_id=None,
        pad_token_id=None,
        eos_token_id=None,
        length_penalty=None,
        no_repeat_ngram_size=None,
        num_return_sequences=None,
        attention_mask=None,
        decoder_start_token_id=None,
        use_cache=None,
        output_scores=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict_in_generate=None,
        forced_bos_token_id=None,
        forced_eos_token_id=None,
        suppress_tokens: Optional[List[int]] = None,
        begin_suppress_tokens: Optional[List[int]] = None,
        forced_decoder_ids: Optional[List[List[int]]] = None,
        **model_kwargs,
    ) -> Union[TFGreedySearchOutput, TFSampleOutput, TFBeamSearchOutput, TFBeamSampleOutput, tf.Tensor]:
        r"""
        Generates sequences for models with a language modeling head. The method currently supports greedy decoding,
        beam-search decoding, sampling with temperature, sampling with top-k or nucleus sampling.

        Adapted in part from [Facebook's XLM beam search
        code](https://github.com/facebookresearch/XLM/blob/9e6f6814d17be4fe5b15f2e6c43eb2b2d76daeb4/src/model/transformer.py

        Apart from `input_ids` and `attention_mask`, all the arguments below will default to the value of the attribute
        of the same name inside the [`PretrainedConfig`] of the model. The default values indicated are the default
        values of those config.

        Most of these parameters are explained in more detail in [this blog
        post](https://huggingface.co/blog/how-to-generate).

        Parameters:
            input_ids (`tf.Tensor` of shape `(batch_size, sequence_length)`, `(batch_size, sequence_length,
            feature_dim)` or `(batch_size, num_channels, height, width)`, *optional*):
                The sequence used as a prompt for the generation or as model inputs to the encoder. If `None` the
                method initializes it with `bos_token_id` and a batch size of 1. For decoder-only models `inputs`
                should of in the format of `input_ids`. For encoder-decoder models *inputs* can represent any of
                `input_ids`, `input_values`, `input_features`, or `pixel_values`.
            max_length (`int`, *optional*, defaults to `model.config.max_length`):
                The maximum length the generated tokens can have. Corresponds to the length of the input prompt +
                `max_new_tokens`. In general, prefer the use of `max_new_tokens`, which ignores the number of tokens in
                the prompt.
            max_new_tokens (`int`, *optional*):
                The maximum numbers of tokens to generate, ignoring the number of tokens in the prompt.
            min_length (`int`, *optional*, defaults to 10):
                The minimum length of the sequence to be generated.
            do_sample (`bool`, *optional*, defaults to `False`):
                Whether or not to use sampling ; use greedy decoding otherwise.
            early_stopping (`bool`, *optional*, defaults to `False`):
                Whether to stop the beam search when at least `num_beams` sentences are finished per batch or not.
            num_beams (`int`, *optional*, defaults to 1):
                Number of beams for beam search. 1 means no beam search.
            temperature (`float`, *optional*, defaults to 1.0):
                The value used to module the next token probabilities.
            top_k (`int`, *optional*, defaults to 50):
                The number of highest probability vocabulary tokens to keep for top-k-filtering.
            top_p (`float`, *optional*, defaults to 1.0):
                If set to float < 1, only the most probable tokens with probabilities that add up to `top_p` or higher
                are kept for generation.
            repetition_penalty (`float`, *optional*, defaults to 1.0):
                The parameter for repetition penalty. 1.0 means no penalty. See [this
                paper](https://arxiv.org/pdf/1909.05858.pdf) for more details.
            pad_token_id (`int`, *optional*):
                The id of the *padding* token.
            bos_token_id (`int`, *optional*):
                The id of the *beginning-of-sequence* token.
            eos_token_id (`int`, *optional*):
                The id of the *end-of-sequence* token.
            length_penalty (`float`, *optional*, defaults to 1.0):
                Exponential penalty to the length that is used with beam-based generation. It is applied as an exponent
                to the sequence length, which in turn is used to divide the score of the sequence. Since the score is
                the log likelihood of the sequence (i.e. negative), `length_penalty` > 0.0 promotes longer sequences,
                while `length_penalty` < 0.0 encourages shorter sequences.
            no_repeat_ngram_size (`int`, *optional*, defaults to 0):
                If set to int > 0, all ngrams of that size can only occur once.
            bad_words_ids(`List[int]`, *optional*):
                List of token ids that are not allowed to be generated. In order to get the tokens of the words that
                should not appear in the generated text, use `tokenizer.encode(bad_word, add_prefix_space=True)`.
            num_return_sequences(`int`, *optional*, defaults to 1):
                The number of independently computed returned sequences for each element in the batch.
            attention_mask (`tf.Tensor` of `dtype=tf.int32` and shape `(batch_size, sequence_length)`, *optional*):
                Mask to avoid performing attention on padding token indices. Mask values are in `[0, 1]`, 1 for tokens
                that are not masked, and 0 for masked tokens.

                If not provided, will default to a tensor the same shape as `input_ids` that masks the pad token.

                [What are attention masks?](../glossary
            decoder_start_token_id (`int`, *optional*):
                If an encoder-decoder model starts decoding with a different token than *bos*, the id of that token.
            use_cache (`bool`, *optional*, defaults to `True`):
                Whether or not the model should use the past last key/values attentions (if applicable to the model) to
                speed up decoding.
            output_attentions (`bool`, *optional*, defaults to `False`):
                Whether or not to return the attentions tensors of all attention layers. See `attentions` under
                returned tensors for more details.
            output_hidden_states (`bool`, *optional*, defaults to `False`):
                Whether or not to return the hidden states of all layers. See `hidden_states` under returned tensors
                for more details.
            output_scores (`bool`, *optional*, defaults to `False`):
                Whether or not to return the prediction scores. See `scores` under returned tensors for more details.
            return_dict_in_generate (`bool`, *optional*, defaults to `False`):
                Whether or not to return a [`~utils.ModelOutput`] instead of a plain tuple.
            forced_bos_token_id (`int`, *optional*):
                The id of the token to force as the first generated token after the `decoder_start_token_id`. Useful
                for multilingual models like [mBART](../model_doc/mbart) where the first generated token needs to be
                the target language token.
            forced_eos_token_id (`int`, *optional*):
                The id of the token to force as the last generated token when `max_length` is reached.
            suppress_tokens  (`List[int]`, *optional*, defaults to `model.config.suppress_tokens`):
                A list of tokens that will be supressed at generation. The `SupressTokens` logit processor will set
                their log probs to `-inf` so that they are not sampled.
            begin_suppress_tokens  (`List[int]`, *optional*, defaults to `model.config.begin_suppress_tokens`):
                A list of tokens that will be supressed at the begining of the generation. The `SupressBeginTokens`
                logit processor will set their log probs to `-inf` so that they are not sampled.
            forced_decoder_ids (`List[List[int]]`, *optional*, defaults to `model.config.forced_decoder_ids`):
                A list of pairs of integers which indicates a mapping from generation indices to token indices that
                will be forced before sampling. For example, `[[1, 123]]` means the second generated token will always
                be a token of index 123.
            model_specific_kwargs:
                Additional model specific kwargs will be forwarded to the `forward` function of the model.

        Return:
            [`~utils.ModelOutput`] or `tf.Tensor`: A [`~utils.ModelOutput`] (if `return_dict_in_generate=True` or when
            `config.return_dict_in_generate=True`) or a `tf.Tensor`.

                If the model is *not* an encoder-decoder model (`model.config.is_encoder_decoder=False`), the possible
                [`~utils.ModelOutput`] types are:

                    - [`~generation_tf_utils.TFGreedySearchDecoderOnlyOutput`],
                    - [`~generation_tf_utils.TFSampleDecoderOnlyOutput`],
                    - [`~generation_tf_utils.TFBeamSearchDecoderOnlyOutput`],
                    - [`~generation_tf_utils.TFBeamSampleDecoderOnlyOutput`]

                If the model is an encoder-decoder model (`model.config.is_encoder_decoder=True`), the possible
                [`~utils.ModelOutput`] types are:

                    - [`~generation_tf_utils.TFGreedySearchEncoderDecoderOutput`],
                    - [`~generation_tf_utils.TFSampleEncoderDecoderOutput`],
                    - [`~generation_tf_utils.TFBeamSearchEncoderDecoderOutput`],
                    - [`~generation_tf_utils.TFBeamSampleEncoderDecoderOutput`]

        Examples:

        ```python
        tokenizer = AutoTokenizer.from_pretrained("distilgpt2")  
        model = TFAutoModelWithLMHead.from_pretrained(
            "distilgpt2"
        )  
        outputs = model.generate(max_length=40)  
        print(f"Generated: {tokenizer.decode(outputs[0], skip_special_tokens=True)}")

        tokenizer = AutoTokenizer.from_pretrained("openai-gpt")  
        model = TFAutoModelWithLMHead.from_pretrained(
            "openai-gpt"
        )  
        input_context = "The dog"
        input_ids = tokenizer.encode(input_context, return_tensors="tf")  
        outputs = model.generate(
            input_ids=input_ids, num_beams=5, num_return_sequences=3, temperature=1.5
        )  
        for i in range(3):  
            print(f"Generated {i}: {tokenizer.decode(outputs[i], skip_special_tokens=True)}")

        tokenizer = AutoTokenizer.from_pretrained("distilgpt2")  
        model = TFAutoModelWithLMHead.from_pretrained(
            "distilgpt2"
        )  
        input_context = "The dog"
        input_ids = tokenizer.encode(input_context, return_tensors="tf")  
        outputs = model.generate(
            input_ids=input_ids, max_length=40, temperature=0.7, num_return_sequences=3, do_sample=True
        )  
        for i in range(3):  
            print(f"Generated {i}: {tokenizer.decode(outputs[i], skip_special_tokens=True)}")

        tokenizer = AutoTokenizer.from_pretrained("ctrl")  
        model = TFAutoModelWithLMHead.from_pretrained(
            "ctrl"
        )  
        input_context = "Legal My neighbor is"  "Legal" is one of the control codes for ctrl
        input_ids = tokenizer.encode(input_context, return_tensors="tf")  
        outputs = model.generate(
            input_ids=input_ids, max_length=50, temperature=0.7, repetition_penalty=1.2
        )  
        print(f"Generated: {tokenizer.decode(outputs[0], skip_special_tokens=True)}")

        tokenizer = AutoTokenizer.from_pretrained("gpt2")  
        model = TFAutoModelWithLMHead.from_pretrained(
            "gpt2"
        )  
        input_context = "My cute dog"
        bad_words_ids = [
            tokenizer.encode(bad_word, add_prefix_space=True) for bad_word in ["idiot", "stupid", "shut up"]
        ]
        input_ids = tokenizer.encode(input_context, return_tensors="tf")  
        outputs = model.generate(
            input_ids=input_ids, max_length=100, do_sample=True, bad_words_ids=bad_words_ids
        )  
        ```"""
        num_beams = num_beams if num_beams is not None else self.config.num_beams
        do_sample = do_sample if do_sample is not None else self.config.do_sample

        if do_sample is False or num_beams == 1:
            seed = model_kwargs.pop("seed", None)
            return self._generate(
                input_ids=input_ids,
                max_length=max_length,
                max_new_tokens=max_new_tokens,
                min_length=min_length,
                do_sample=do_sample,
                early_stopping=early_stopping,
                num_beams=num_beams,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
                bad_words_ids=bad_words_ids,
                bos_token_id=bos_token_id,
                pad_token_id=pad_token_id,
                eos_token_id=eos_token_id,
                length_penalty=length_penalty,
                no_repeat_ngram_size=no_repeat_ngram_size,
                num_return_sequences=num_return_sequences,
                attention_mask=attention_mask,
                decoder_start_token_id=decoder_start_token_id,
                use_cache=use_cache,
                seed=seed,
                output_scores=output_scores,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
                return_dict_in_generate=return_dict_in_generate,
                forced_bos_token_id=forced_bos_token_id,
                forced_eos_token_id=forced_eos_token_id,
                suppress_tokens=suppress_tokens,
                begin_suppress_tokens=begin_suppress_tokens,
                forced_decoder_ids=forced_decoder_ids,
                **model_kwargs,
            )

        
        if self.get_output_embeddings() is None:
            raise AttributeError(
                "You tried to generate sequences with a model that does not have a LM Head. Please use another model"
                " class (e.g. `TFOpenAIGPTLMHeadModel`, `TFXLNetLMHeadModel`, `TFGPT2LMHeadModel`,"
                " `TFCTRLLMHeadModel`, `TFT5ForConditionalGeneration`, `TFTransfoXLLMHeadModel`)"
            )

        max_length = max_length if max_length is not None else self.config.max_length
        min_length = min_length if min_length is not None else self.config.min_length
        early_stopping = early_stopping if early_stopping is not None else self.config.early_stopping
        temperature = temperature if temperature is not None else self.config.temperature
        top_k = top_k if top_k is not None else self.config.top_k
        top_p = top_p if top_p is not None else self.config.top_p

        repetition_penalty = repetition_penalty if repetition_penalty is not None else self.config.repetition_penalty
        bos_token_id = bos_token_id if bos_token_id is not None else self.config.bos_token_id
        pad_token_id = pad_token_id if pad_token_id is not None else self.config.pad_token_id
        eos_token_id = eos_token_id if eos_token_id is not None else self.config.eos_token_id
        length_penalty = length_penalty if length_penalty is not None else self.config.length_penalty
        no_repeat_ngram_size = (
            no_repeat_ngram_size if no_repeat_ngram_size is not None else self.config.no_repeat_ngram_size
        )
        bad_words_ids = bad_words_ids if bad_words_ids is not None else self.config.bad_words_ids
        num_return_sequences = (
            num_return_sequences if num_return_sequences is not None else self.config.num_return_sequences
        )
        decoder_start_token_id = (
            decoder_start_token_id if decoder_start_token_id is not None else self.config.decoder_start_token_id
        )
        forced_bos_token_id = (
            forced_bos_token_id if forced_bos_token_id is not None else self.config.forced_bos_token_id
        )
        forced_eos_token_id = (
            forced_eos_token_id if forced_eos_token_id is not None else self.config.forced_eos_token_id
        )
        suppress_tokens = suppress_tokens if suppress_tokens is not None else self.config.suppress_tokens
        begin_suppress_tokens = (
            begin_suppress_tokens if begin_suppress_tokens is not None else self.config.begin_suppress_tokens
        )
        if forced_decoder_ids is None and hasattr(self.config, "forced_decoder_ids"):
            forced_decoder_ids = self.config.forced_decoder_ids

        output_scores = output_scores if output_scores is not None else self.config.output_scores
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict_in_generate = (
            return_dict_in_generate if return_dict_in_generate is not None else self.config.return_dict_in_generate
        )

        model_kwargs["output_scores"] = output_scores
        model_kwargs["output_attentions"] = output_attentions
        model_kwargs["output_hidden_states"] = output_hidden_states
        if self.config.is_encoder_decoder:
            model_kwargs["encoder_attentions"] = None
            model_kwargs["encoder_hidden_states"] = None

        if input_ids is not None:
            batch_size = shape_list(input_ids)[0]  
        else:
            batch_size = 1

        assert isinstance(max_length, int) and max_length > 0, "`max_length` should be a strictly positive integer."
        assert isinstance(min_length, int) and min_length >= 0, "`min_length` should be a positive integer."
        assert isinstance(do_sample, bool), "`do_sample` should be a boolean."
        assert isinstance(early_stopping, bool), "`early_stopping` should be a boolean."
        assert isinstance(num_beams, int) and num_beams > 0, "`num_beams` should be a strictly positive integer."
        assert temperature > 0, "`temperature` should be strictly positive."
        assert isinstance(top_k, int) and top_k >= 0, "`top_k` should be a positive integer."
        assert 0 <= top_p <= 1, "`top_p` should be between 0 and 1."
        assert repetition_penalty >= 1.0, "`repetition_penalty` should be >= 1."
        assert input_ids is not None or (
            isinstance(bos_token_id, int) and bos_token_id >= 0
        ), "If input_ids is not defined, `bos_token_id` should be a positive integer."
        assert pad_token_id is None or (
            isinstance(pad_token_id, int) and (pad_token_id >= 0)
        ), "`pad_token_id` should be a positive integer."
        assert (eos_token_id is None) or (
            isinstance(eos_token_id, int) and (eos_token_id >= 0)
        ), "`eos_token_id` should be a positive integer."
        assert length_penalty > 0, "`length_penalty` should be strictly positive."
        assert (
            isinstance(num_return_sequences, int) and num_return_sequences > 0
        ), "`num_return_sequences` should be a strictly positive integer."
        assert (
            bad_words_ids is None or isinstance(bad_words_ids, list) and isinstance(bad_words_ids[0], list)
        ), "`bad_words_ids` is either `None` or a list of lists of tokens that should not be generated"

        
        "input_ids = self._prepare_input_ids_for_generation(bos_token_id, model_kwargs.get("encoder_outputs"))"
        
        
        
        
        if input_ids is None:
            assert isinstance(bos_token_id, int) and bos_token_id >= 0, (
                "you should either supply a context to complete as `input_ids` input "
                "or a `bos_token_id` (integer >= 0) as a first token to start the generation."
            )
            input_ids = tf.fill((batch_size, 1), bos_token_id)

        
        if do_sample is False:
            if num_beams == 1:
                
                assert num_return_sequences == 1, (
                    "Greedy decoding will always produce the same output for num_beams == 1 and num_return_sequences >"
                    " 1. Please set num_return_sequences = 1"
                )

            else:
                
                assert num_beams >= num_return_sequences, (
                    "Greedy beam search decoding cannot return more sequences than it has beams. Please set num_beams"
                    " >= num_return_sequences"
                )

        
        accepts_attention_mask = "attention_mask" in set(inspect.signature(self.call).parameters.keys())
        if accepts_attention_mask:
            if (attention_mask is None) and (pad_token_id is not None) and (pad_token_id in input_ids.numpy()):
                attention_mask = tf.cast(tf.math.not_equal(input_ids, pad_token_id), dtype=tf.int32)
            elif attention_mask is None:
                attention_mask = tf.ones(shape_list(input_ids)[:2], dtype=tf.int32)

        if pad_token_id is None and eos_token_id is not None:
            logger.warning(f"Setting `pad_token_id` to {eos_token_id} (first `eos_token_id`) to generate sequence")
            pad_token_id = eos_token_id

        
        cur_len = shape_list(input_ids)[1]  
        vocab_size = getattr(self.config, "vocab_size", None)
        if vocab_size is None and self.config.is_encoder_decoder:
            decoder_config = getattr(self.config, "decoder", None)
            if decoder_config is not None:
                vocab_size = getattr(self.config.decoder, "vocab_size", None)

        
        if do_sample:
            effective_batch_size = batch_size * num_return_sequences
            effective_batch_mult = num_return_sequences
        else:
            effective_batch_size = batch_size
            effective_batch_mult = 1

        if self.config.is_encoder_decoder:
            if decoder_start_token_id is None:
                decoder_start_token_id = bos_token_id

            assert (
                decoder_start_token_id is not None
            ), "decoder_start_token_id or bos_token_id has to be defined for encoder-decoder generation"
            assert hasattr(self, "get_encoder"), f"{self} should have a 'get_encoder' function defined"
            assert callable(self.get_encoder), f"{self.get_encoder} should be a method"

            
            encoder = self.get_encoder()

            encoder_kwargs = {
                "output_attentions": output_attentions,
                "output_hidden_states": output_hidden_states,
                "return_dict": return_dict_in_generate,
            }
            if accepts_attention_mask:
                encoder_kwargs["attention_mask"] = attention_mask

            encoder_outputs = encoder(input_ids, **encoder_kwargs)
            if return_dict_in_generate:
                if output_attentions:
                    model_kwargs["encoder_attentions"] = encoder_outputs.attentions
                if output_hidden_states:
                    model_kwargs["encoder_hidden_states"] = encoder_outputs.hidden_states

        expanded_batch_idxs = tf.reshape(
            tf.repeat(tf.expand_dims(tf.range(batch_size), -1), repeats=num_beams * effective_batch_mult, axis=1),
            shape=(-1,),
        )
        
        if len(shape_list(input_ids)) == 2:
            input_ids = tf.gather(input_ids, expanded_batch_idxs, axis=0)
        if accepts_attention_mask:
            attention_mask = tf.gather(attention_mask, expanded_batch_idxs, axis=0)

        if self.config.is_encoder_decoder:

            
            input_ids = (
                tf.ones(
                    (effective_batch_size * num_beams, 1),
                    dtype=tf.int32,
                )
                * decoder_start_token_id
            )
            cur_len = 1

            assert (
                batch_size == encoder_outputs[0].shape[0]
            ), f"expected encoder_outputs[0] to have 1st dimension bs={batch_size}, got {encoder_outputs[0].shape[0]} "

            
            encoder_outputs = (tf.gather(encoder_outputs[0], expanded_batch_idxs, axis=0),)
        else:
            encoder_outputs = None
            cur_len = shape_list(input_ids)[-1]

        assert cur_len < max_length, (
            f"The context has {cur_len} number of tokens, but `max_length` is only {max_length}. Please make sure that"
            " `max_length` is bigger than the number of tokens, by setting either `generate(max_length=...,...)` or"
            " `config.max_length = ...`"
        )

        return self._generate_beam_search(
            input_ids,
            cur_len=cur_len,
            max_length=max_length,
            min_length=min_length,
            do_sample=do_sample,
            early_stopping=early_stopping,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            no_repeat_ngram_size=no_repeat_ngram_size,
            bad_words_ids=bad_words_ids,
            pad_token_id=pad_token_id,
            eos_token_id=eos_token_id,
            batch_size=effective_batch_size,
            num_return_sequences=num_return_sequences,
            length_penalty=length_penalty,
            num_beams=num_beams,
            vocab_size=vocab_size,
            encoder_outputs=encoder_outputs,
            attention_mask=attention_mask,
            use_cache=use_cache,
            forced_bos_token_id=forced_bos_token_id,
            forced_eos_token_id=forced_eos_token_id,
            return_dict_in_generate=return_dict_in_generate,
            **model_kwargs,
        )

    def _generate_beam_search(
        self,
        input_ids,
        cur_len,
        max_length,
        min_length,
        do_sample,
        early_stopping,
        temperature,
        top_k,
        top_p,
        repetition_penalty,
        no_repeat_ngram_size,
        bad_words_ids,
        pad_token_id,
        eos_token_id,
        batch_size,
        num_return_sequences,
        length_penalty,
        num_beams,
        vocab_size,
        encoder_outputs,
        attention_mask,
        use_cache,
        forced_bos_token_id,
        forced_eos_token_id,
        return_dict_in_generate,
        **kwargs,
    ) -> Union[TFBeamSearchOutput, TFBeamSampleOutput, tf.Tensor]:
        """Generate sequences for each example with beam search."""

        
        generated_hyps = [
            BeamHypotheses(num_beams, max_length, length_penalty, early_stopping=early_stopping)
            for _ in range(batch_size)
        ]

        
        if do_sample is False:
            beam_scores_begin = tf.zeros((batch_size, 1), dtype=tf.float32)
            beam_scores_end = tf.ones((batch_size, num_beams - 1), dtype=tf.float32) * (-1e9)
            beam_scores = tf.concat([beam_scores_begin, beam_scores_end], -1)
        else:
            beam_scores = tf.zeros((batch_size, num_beams), dtype=tf.float32)

        beam_scores = tf.reshape(beam_scores, (batch_size * num_beams,))

        
        past = None

        
        scores = () if (return_dict_in_generate and kwargs["output_scores"]) else None
        decoder_attentions = () if (return_dict_in_generate and kwargs["output_attentions"]) else None
        cross_attentions = () if (return_dict_in_generate and kwargs["output_attentions"]) else None
        decoder_hidden_states = () if (return_dict_in_generate and kwargs["output_hidden_states"]) else None
        
        if self.config.is_encoder_decoder:
            encoder_attentions = (
                kwargs["encoder_attentions"] if (return_dict_in_generate and kwargs["encoder_attentions"]) else None
            )
            encoder_hidden_states = (
                kwargs["encoder_hidden_states"]
                if (return_dict_in_generate and kwargs["encoder_hidden_states"])
                else None
            )
            
            
            
            if encoder_hidden_states is not None:
                encoder_outputs = (*encoder_outputs, encoder_hidden_states)
            if encoder_attentions is not None:
                encoder_outputs = (*encoder_outputs, encoder_attentions)

        
        done = [False for _ in range(batch_size)]

        while cur_len < max_length:
            model_inputs = self.prepare_inputs_for_generation(
                input_ids,
                past=past,
                attention_mask=attention_mask,
                use_cache=use_cache,
                encoder_outputs=encoder_outputs,
                **kwargs,
            )
            outputs = self(
                **model_inputs,
                return_dict=True,
                output_attentions=kwargs["output_attentions"],
                output_hidden_states=kwargs["output_hidden_states"],
            )
            next_token_logits = outputs.logits[:, -1, :]  

            
            if self._use_cache(outputs, use_cache):
                past = outputs[1]

            
            if repetition_penalty != 1.0:
                next_token_logits_penalties = _create_next_token_logits_penalties(
                    input_ids, next_token_logits, repetition_penalty
                )
                next_token_logits = tf.math.multiply(next_token_logits, next_token_logits_penalties)

            
            if temperature != 1.0:
                next_token_logits = next_token_logits / temperature

            if self.config.is_encoder_decoder and do_sample is False:
                next_token_logits = self.adjust_logits_during_generation(
                    next_token_logits,
                    cur_len=cur_len,
                    max_length=max_length,
                    forced_bos_token_id=forced_bos_token_id,
                    forced_eos_token_id=forced_eos_token_id,
                )
            
            scores = tf.nn.log_softmax(next_token_logits, axis=-1)  

            
            if eos_token_id is not None and cur_len < min_length:
                
                num_batch_hypotheses = batch_size * num_beams

                is_token_logit_eos_token = tf.convert_to_tensor(
                    [True if token == eos_token_id else False for token in range(vocab_size)], dtype=tf.bool
                )
                eos_token_indices_mask = tf.broadcast_to(is_token_logit_eos_token, [num_batch_hypotheses, vocab_size])
                scores = tf.where(eos_token_indices_mask, -float("inf"), scores)

            if no_repeat_ngram_size > 0:
                
                
                num_batch_hypotheses = batch_size * num_beams
                banned_tokens = calc_banned_ngram_tokens(
                    input_ids, num_batch_hypotheses, no_repeat_ngram_size, cur_len
                )
                
                banned_tokens_indices_mask = []
                for banned_tokens_slice in banned_tokens:
                    banned_tokens_indices_mask.append(
                        [True if token in banned_tokens_slice else False for token in range(vocab_size)]
                    )

                scores = tf.where(
                    tf.convert_to_tensor(banned_tokens_indices_mask, dtype=tf.bool), -float("inf"), scores
                )

            if bad_words_ids is not None:
                
                banned_tokens = calc_banned_bad_words_ids(input_ids, bad_words_ids)

                banned_tokens_indices_mask = []
                for banned_tokens_slice in banned_tokens:
                    banned_tokens_indices_mask.append(
                        [True if token in banned_tokens_slice else False for token in range(vocab_size)]
                    )

                scores = tf.where(
                    tf.convert_to_tensor(banned_tokens_indices_mask, dtype=tf.bool), -float("inf"), scores
                )

            assert shape_list(scores) == [batch_size * num_beams, vocab_size]

            if do_sample:
                _scores = scores + tf.broadcast_to(
                    beam_scores[:, None], (batch_size * num_beams, vocab_size)
                )  

                
                _scores = tf_top_k_top_p_filtering(
                    _scores, top_k=top_k, top_p=top_p, min_tokens_to_keep=2
                )  
                
                _scores = tf.reshape(_scores, (batch_size, num_beams * vocab_size))

                next_tokens = sample_without_replacement(
                    _scores, num_samples=2 * num_beams
                )  
                
                next_scores = tf.gather(_scores, next_tokens, batch_dims=1)  

                
                next_scores_indices = tf.argsort(next_scores, direction="DESCENDING", axis=1)
                next_scores = tf.gather(next_scores, next_scores_indices, batch_dims=1)  
                next_tokens = tf.gather(next_tokens, next_scores_indices, batch_dims=1)  
            else:
                
                next_scores = scores + tf.broadcast_to(
                    beam_scores[:, None], (batch_size * num_beams, vocab_size)
                )  

                
                next_scores = tf.reshape(
                    next_scores, (batch_size, num_beams * vocab_size)
                )  

                next_scores, next_tokens = tf.math.top_k(next_scores, k=2 * num_beams, sorted=True)

            assert shape_list(next_scores) == shape_list(next_tokens) == [batch_size, 2 * num_beams]

            
            if return_dict_in_generate:
                if kwargs["output_scores"]:
                    scores += (next_token_logits,)
                if kwargs["output_attentions"]:
                    decoder_attentions += (
                        (outputs.decoder_attentions,) if self.config.is_encoder_decoder else (outputs.attentions,)
                    )
                    if self.config.is_encoder_decoder:
                        cross_attentions += (outputs.cross_attentions,)

                if kwargs["output_hidden_states"]:
                    decoder_hidden_states += (
                        (outputs.decoder_hidden_states,)
                        if self.config.is_encoder_decoder
                        else (outputs.hidden_states,)
                    )

            
            next_batch_beam = []

            
            for batch_idx in range(batch_size):

                
                if done[batch_idx]:
                    assert (
                        len(generated_hyps[batch_idx]) >= num_beams
                    ), f"Batch can only be done if at least {num_beams} beams have been generated."
                    assert (
                        eos_token_id is not None and pad_token_id is not None
                    ), "generated beams >= num_beams -> eos_token_id and pad_token have to be defined"
                    next_batch_beam.extend([(0, pad_token_id, 0)] * num_beams)  
                    continue

                
                next_sent_beam = []

                
                for beam_token_rank, (beam_token_id, beam_token_score) in enumerate(
                    zip(next_tokens[batch_idx], next_scores[batch_idx])
                ):
                    
                    beam_id = beam_token_id // vocab_size
                    token_id = beam_token_id % vocab_size

                    effective_beam_id = batch_idx * num_beams + beam_id
                    
                    if (eos_token_id is not None) and (token_id.numpy() == eos_token_id):
                        
                        is_beam_token_worse_than_top_num_beams = beam_token_rank >= num_beams
                        if is_beam_token_worse_than_top_num_beams:
                            continue
                        generated_hyps[batch_idx].add(
                            tf.identity(input_ids[effective_beam_id]), beam_token_score.numpy()
                        )
                    else:
                        
                        next_sent_beam.append((beam_token_score, token_id, effective_beam_id))

                    
                    if len(next_sent_beam) == num_beams:
                        break

                
                done[batch_idx] = done[batch_idx] or generated_hyps[batch_idx].is_done(
                    tf.reduce_max(next_scores[batch_idx]).numpy(), cur_len
                )

                
                assert len(next_sent_beam) == num_beams, "Beam should always be full"
                next_batch_beam.extend(next_sent_beam)
                assert len(next_batch_beam) == num_beams * (batch_idx + 1)

            
            if all(done):
                break

            
            assert len(next_batch_beam) == batch_size * num_beams
            beam_scores = tf.convert_to_tensor([x[0] for x in next_batch_beam], dtype=tf.float32)
            beam_tokens = tf.convert_to_tensor([x[1] for x in next_batch_beam], dtype=tf.int32)
            beam_idx = tf.convert_to_tensor([x[2] for x in next_batch_beam], dtype=tf.int32)

            
            input_ids = tf.stack([tf.identity(input_ids[x, :]) for x in beam_idx])
            input_ids = tf.concat([input_ids, tf.expand_dims(beam_tokens, 1)], axis=-1)
            cur_len = cur_len + 1

            
            if past is not None:
                past = self._reorder_cache(past, beam_idx)

            
            if self.config.is_encoder_decoder is False:
                attention_mask = tf.concat(
                    [attention_mask, tf.ones((shape_list(attention_mask)[0], 1), dtype=tf.int32)], axis=-1
                )

        
        for batch_idx in range(batch_size):
            
            if done[batch_idx]:
                continue
            
            if eos_token_id is not None and all(
                (token_id % vocab_size).numpy().item() != eos_token_id for token_id in next_tokens[batch_idx]
            ):
                if not tf.reduce_all(
                    next_scores[batch_idx, :num_beams] == tf.reshape(beam_scores, (batch_size, num_beams))[batch_idx]
                ):
                    raise ValueError(
                        f"If batch_idx is not done, final next scores: {next_scores[:, :num_beams][batch_idx]} have "
                        "to equal to accumulated beam_scores: "
                        f"{tf.reshape(beam_scores, (batch_size, num_beams))[batch_idx]}"
                    )
            
            for beam_id in range(num_beams):
                effective_beam_id = batch_idx * num_beams + beam_id
                final_score = beam_scores[effective_beam_id].numpy().item()
                final_tokens = input_ids[effective_beam_id]
                generated_hyps[batch_idx].add(final_tokens, final_score)

        
        output_batch_size = batch_size if do_sample else batch_size * num_return_sequences
        output_num_return_sequences_per_batch = 1 if do_sample else num_return_sequences

        
        sent_lengths_list = []
        best = []

        
        for i, hypotheses in enumerate(generated_hyps):
            sorted_hyps = sorted(hypotheses.beams, key=lambda x: x[0])
            for j in range(output_num_return_sequences_per_batch):
                best_hyp = sorted_hyps.pop()[1]
                sent_lengths_list.append(len(best_hyp))
                best.append(best_hyp)
        assert output_batch_size == len(
            best
        ), f"Output batch size {output_batch_size} must match output beam hypotheses {len(best)}"

        sent_lengths = tf.convert_to_tensor(sent_lengths_list, dtype=tf.int32)

        
        if tf.reduce_min(sent_lengths).numpy() != tf.reduce_max(sent_lengths).numpy():
            assert pad_token_id is not None, "`Pad_token_id` has to be defined"
            sent_max_len = min(tf.reduce_max(sent_lengths).numpy() + 1, max_length)
            decoded_list = []

            
            for i, hypo in enumerate(best):
                assert sent_lengths[i] == shape_list(hypo)[0]
                
                if sent_lengths[i] == sent_max_len:
                    decoded_slice = hypo
                else:
                    
                    num_pad_tokens = sent_max_len - sent_lengths[i]
                    padding = pad_token_id * tf.ones((num_pad_tokens,), dtype=tf.int32)
                    decoded_slice = tf.concat([hypo, padding], axis=-1)

                    
                    if sent_lengths[i] < max_length:
                        decoded_slice = tf.where(
                            tf.range(sent_max_len, dtype=tf.int32) == sent_lengths[i],
                            eos_token_id * tf.ones((sent_max_len,), dtype=tf.int32),
                            decoded_slice,
                        )
                
                decoded_list.append(decoded_slice)

            decoded = tf.stack(decoded_list)
        else:
            
            assert (len(hypo) == max_length for hypo in best)
            decoded = tf.stack(best)

        if return_dict_in_generate:
            if do_sample and self.config.is_encoder_decoder:
                return TFBeamSampleEncoderDecoderOutput(
                    sequences=decoded,
                    scores=scores,
                    encoder_attentions=encoder_attentions,
                    encoder_hidden_states=encoder_hidden_states,
                    decoder_attentions=decoder_attentions,
                    cross_attentions=cross_attentions,
                    decoder_hidden_states=decoder_hidden_states,
                )
            elif do_sample and not self.config.is_encoder_decoder:
                return TFBeamSampleDecoderOnlyOutput(
                    sequences=decoded,
                    scores=scores,
                    attentions=decoder_attentions,
                    hidden_states=decoder_hidden_states,
                )
            elif self.config.is_encoder_decoder:
                return TFBeamSearchEncoderDecoderOutput(
                    sequences=decoded,
                    scores=scores,
                    encoder_attentions=encoder_attentions,
                    encoder_hidden_states=encoder_hidden_states,
                    decoder_attentions=decoder_attentions,
                    cross_attentions=cross_attentions,
                    decoder_hidden_states=decoder_hidden_states,
                )
            else:
                return TFBeamSearchDecoderOnlyOutput(
                    sequences=decoded,
                    scores=scores,
                    attentions=decoder_attentions,
                    hidden_states=decoder_hidden_states,
                )
        else:
            return decoded

    @staticmethod
    def _reorder_cache(past, beam_idx):
        return tuple(tf.gather(layer_past, beam_idx, axis=1) for layer_past in past)

    def adjust_logits_during_generation(
        self, logits, cur_len, max_length, forced_bos_token_id, forced_eos_token_id, **kwargs
    ):
        """
        Implement in subclasses of [`PreTrainedModel`] for custom behavior to adjust the logits in the generate method.
        """
        vocab_size = getattr(self.config, "vocab_size", None)
        if vocab_size is None and self.config.is_encoder_decoder:
            decoder_config = getattr(self.config, "decoder", None)
            if decoder_config is not None:
                vocab_size = getattr(self.config.decoder, "vocab_size", None)

        if cur_len == 1 and forced_bos_token_id is not None:
            vocab_range = tf.constant(range(vocab_size))
            return tf.where(vocab_range != forced_bos_token_id, -1e8, logits)
        elif cur_len == max_length - 1 and forced_eos_token_id is not None:
            vocab_range = tf.constant(range(vocab_size))
            return tf.where(vocab_range != forced_eos_token_id, -1e8, logits)
        else:
            return logits

    def _validate_model_class(self):
        """
        Confirms that the model class is compatible with generation. If not, raises an exception that points to the
        right class to use.
        """
        if not hasattr(self, "prepare_inputs_for_generation"):
            generate_compatible_mappings = [
                TF_MODEL_FOR_CAUSAL_LM_MAPPING,
                TF_MODEL_FOR_VISION_2_SEQ_MAPPING,
                TF_MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING,
                TF_MODEL_FOR_SPEECH_SEQ_2_SEQ_MAPPING,
            ]
            generate_compatible_classes = set()
            for model_mapping in generate_compatible_mappings:
                supported_models = model_mapping.get(type(self.config), default=None)
                if supported_models is not None:
                    generate_compatible_classes.add(supported_models.__name__)
            exception_message = (
                f"The current model class ({self.__class__.__name__}) is not compatible with `.generate()`, as "
                "it doesn't have a language model head."
            )
            if generate_compatible_classes:
                exception_message += f" Please use one of the following classes instead: {generate_compatible_classes}"
            raise TypeError(exception_message)

    def _validate_model_kwargs(self, model_kwargs: Dict[str, Any]):
        """Validates model kwargs for generation. Generate argument typos will also be caught here."""
        
        if self.config.is_encoder_decoder:
            for key in ["decoder_input_ids"]:
                model_kwargs.pop(key, None)

        unused_model_args = []
        model_args = set(inspect.signature(self.prepare_inputs_for_generation).parameters)
        
        
        if "kwargs" in model_args:
            model_args |= set(inspect.signature(self.call).parameters)
        for key, value in model_kwargs.items():
            if value is not None and key not in model_args:
                unused_model_args.append(key)

        if unused_model_args:
            raise ValueError(
                f"The following `model_kwargs` are not used by the model: {unused_model_args} (note: typos in the"
                " generate arguments will also show up in this list)"
            )

    def _generate(
        self,
        input_ids=None,
        max_length=None,
        max_new_tokens=None,
        min_length=None,
        do_sample=None,
        early_stopping=None,
        num_beams=None,
        temperature=None,
        top_k=None,
        top_p=None,
        repetition_penalty=None,
        bad_words_ids=None,
        bos_token_id=None,
        pad_token_id=None,
        eos_token_id=None,
        length_penalty=None,
        no_repeat_ngram_size=None,
        num_return_sequences=None,
        attention_mask=None,
        decoder_start_token_id=None,
        use_cache=None,
        seed=None,
        output_scores=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict_in_generate=None,
        forced_bos_token_id=None,
        forced_eos_token_id=None,
        suppress_tokens=None,
        begin_suppress_tokens=None,
        forced_decoder_ids=None,
        **model_kwargs,
    ) -> Union[TFGreedySearchOutput, TFSampleOutput, TFBeamSearchOutput, TFBeamSampleOutput, tf.Tensor]:
        r"""
        Generates sequences for models with a language modeling head. The method currently supports greedy decoding,
        beam-search decoding, sampling with temperature, sampling with top-k or nucleus sampling.

        Adapted in part from [Facebook's XLM beam search
        code](https://github.com/facebookresearch/XLM/blob/9e6f6814d17be4fe5b15f2e6c43eb2b2d76daeb4/src/model/transformer.py

        Apart from `input_ids` and `attention_mask`, all the arguments below will default to the value of the attribute
        of the same name inside the [`PretrainedConfig`] of the model. The default values indicated are the default
        values of those config.

        Most of these parameters are explained in more detail in [this blog
        post](https://huggingface.co/blog/how-to-generate).

        Parameters:
            input_ids (`tf.Tensor` of `dtype=tf.int32` and shape `(batch_size, sequence_length)`, *optional*):
                The sequence used as a prompt for the generation. If `None` the method initializes it with
                `bos_token_id` and a batch size of 1.
            max_length (`int`, *optional*, defaults to `model.config.max_length`):
                The maximum length the generated tokens can have. Corresponds to the length of the input prompt +
                `max_new_tokens`. In general, prefer the use of `max_new_tokens`, which ignores the number of tokens in
                the prompt.
            max_new_tokens (`int`, *optional*):
                The maximum numbers of tokens to generate, ignoring the number of tokens in the prompt.
            min_length (`int`, *optional*, defaults to 10):
                The minimum length of the sequence to be generated.
            do_sample (`bool`, *optional*, defaults to `False`):
                Whether or not to use sampling ; use greedy decoding otherwise.
            early_stopping (`bool`, *optional*, defaults to `False`):
                Whether to stop the beam search when at least `num_beams` sentences are finished per batch or not.
            num_beams (`int`, *optional*, defaults to 1):
                Number of beams for beam search. 1 means no beam search.
            temperature (`float`, *optional*, defaults to 1.0):
                The value used to module the next token probabilities.
            top_k (`int`, *optional*, defaults to 50):
                The number of highest probability vocabulary tokens to keep for top-k-filtering.
            top_p (`float`, *optional*, defaults to 1.0):
                If set to float < 1, only the most probable tokens with probabilities that add up to `top_p` or higher
                are kept for generation.
            repetition_penalty (`float`, *optional*, defaults to 1.0):
                The parameter for repetition penalty. 1.0 means no penalty. See [this
                paper](https://arxiv.org/pdf/1909.05858.pdf) for more details.
            pad_token_id (`int`, *optional*):
                The id of the *padding* token.
            bos_token_id (`int`, *optional*):
                The id of the *beginning-of-sequence* token.
            eos_token_id (`int`, *optional*):
                The id of the *end-of-sequence* token.
            length_penalty (`float`, *optional*, defaults to 1.0):
                Exponential penalty to the length that is used with beam-based generation. It is applied as an exponent
                to the sequence length, which in turn is used to divide the score of the sequence. Since the score is
                the log likelihood of the sequence (i.e. negative), `length_penalty` > 0.0 promotes longer sequences,
                while `length_penalty` < 0.0 encourages shorter sequences.
            no_repeat_ngram_size (`int`, *optional*, defaults to 0):
                If set to int > 0, all ngrams of that size can only occur once.
            bad_words_ids(`List[int]`, *optional*):
                List of token ids that are not allowed to be generated. In order to get the tokens of the words that
                should not appear in the generated text, use `tokenizer.encode(bad_word, add_prefix_space=True)`.
            num_return_sequences(`int`, *optional*, defaults to 1):
                The number of independently computed returned sequences for each element in the batch.
            attention_mask (`tf.Tensor` of `dtype=tf.int32` and shape `(batch_size, sequence_length)`, *optional*):
                Mask to avoid performing attention on padding token indices. Mask values are in `[0, 1]`, 1 for tokens
                that are not masked, and 0 for masked tokens.

                If not provided, will default to a tensor the same shape as `input_ids` that masks the pad token.

                [What are attention masks?](../glossary
            decoder_start_token_id (`int`, *optional*):
                If an encoder-decoder model starts decoding with a different token than *bos*, the id of that token.
            use_cache (`bool`, *optional*, defaults to `True`):
                Whether or not the model should use the past last key/values attentions (if applicable to the model) to
                speed up decoding.
            seed (`List[int]`, *optional*):
                Random seed to control sampling, containing two integers, used when `do_sample` is `True`. See the
                `seed` argument from stateless functions in `tf.random`.
            output_attentions (`bool`, *optional*, defaults to `False`):
                Whether or not to return the attentions tensors of all attention layers. See `attentions` under
                returned tensors for more details.
            output_hidden_states (`bool`, *optional*, defaults to `False`):
                Whether or not to return the hidden states of all layers. See `hidden_states` under returned tensors
                for more details.
            output_scores (`bool`, *optional*, defaults to `False`):
                Whether or not to return the prediction scores. See `scores` under returned tensors for more details.
            return_dict_in_generate (`bool`, *optional*, defaults to `False`):
                Whether or not to return a [`~utils.ModelOutput`] instead of a plain tuple.
            forced_bos_token_id (`int`, *optional*):
                The id of the token to force as the first generated token after the `decoder_start_token_id`. Useful
                for multilingual models like [mBART](../model_doc/mbart) where the first generated token needs to be
                the target language token.
            forced_eos_token_id (`int`, *optional*):
                The id of the token to force as the last generated token when `max_length` is reached.
            suppress_tokens  (`List[int]`, *optional*, defaults to `model.config.suppress_tokens`):
                A list of tokens that will be supressed at generation. The `SupressTokens` logit processor will set
                their log probs to `-inf` so that they are not sampled.
            begin_suppress_tokens  (`List[int]`, *optional*, defaults to `model.config.begin_suppress_tokens`):
                A list of tokens that will be supressed at the begining of the generation. The `SupressBeginTokens`
                logit processor will set their log probs to `-inf` so that they are not sampled.
            forced_decoder_ids (`List[List[int]]`, *optional*, defaults to `model.config.forced_decoder_ids`):
                A list of pairs of integers which indicates a mapping from generation indices to token indices that
                will be forced before sampling. For example, `[[1, 123]]` means the second generated token will always
                be a token of index 123.
            model_kwargs:
                Additional model specific kwargs will be forwarded to the `call` function of the model.

        Return:
            [`~utils.ModelOutput`] or `tf.Tensor`: A [`~utils.ModelOutput`] (if `return_dict_in_generate=True` or when
            `config.return_dict_in_generate=True`) or a `tf.Tensor`.

                If the model is *not* an encoder-decoder model (`model.config.is_encoder_decoder=False`), the possible
                [`~utils.ModelOutput`] types are:

                    - [`~generation_tf_utils.TFGreedySearchDecoderOnlyOutput`],
                    - [`~generation_tf_utils.TFSampleDecoderOnlyOutput`],
                    - [`~generation_tf_utils.TFBeamSearchDecoderOnlyOutput`],
                    - [`~generation_tf_utils.TFBeamSampleDecoderOnlyOutput`]

                If the model is an encoder-decoder model (`model.config.is_encoder_decoder=True`), the possible
                [`~utils.ModelOutput`] types are:

                    - [`~generation_tf_utils.TFGreedySearchEncoderDecoderOutput`],
                    - [`~generation_tf_utils.TFSampleEncoderDecoderOutput`],
                    - [`~generation_tf_utils.TFBeamSearchEncoderDecoderOutput`],
                    - [`~generation_tf_utils.TFBeamSampleEncoderDecoderOutput`]

        Examples:

        ```python
        tokenizer = AutoTokenizer.from_pretrained("distilgpt2")  
        model = TFAutoModelWithLMHead.from_pretrained("distilgpt2")
        
        outputs = model.generate(max_length=40)
        print(f"Generated: {tokenizer.decode(outputs[0], skip_special_tokens=True)}")

        tokenizer = AutoTokenizer.from_pretrained("openai-gpt")
        model = TFAutoModelWithLMHead.from_pretrained("openai-gpt")
        input_context = "The dog"
        input_ids = tokenizer.encode(input_context, return_tensors="tf")  
        
        outputs = model.generate(input_ids=input_ids, num_beams=5, num_return_sequences=3, temperature=1.5)
        
        for i in range(3):
            print(f"Generated {i}: {tokenizer.decode(outputs[i], skip_special_tokens=True)}")

        tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
        model = TFAutoModelWithLMHead.from_pretrained("distilgpt2")
        input_context = "The dog"
        input_ids = tokenizer.encode(input_context, return_tensors="tf")
        
        outputs = model.generate(
            input_ids=input_ids, max_length=40, temperature=0.7, num_return_sequences=3, do_sample=True
        )
        
        for i in range(3):
            print(f"Generated {i}: {tokenizer.decode(outputs[i], skip_special_tokens=True)}")

        tokenizer = AutoTokenizer.from_pretrained("ctrl")
        model = TFAutoModelWithLMHead.from_pretrained("ctrl")
        "Legal" is one of the control codes for ctrl
        input_context = "Legal My neighbor is"
        input_ids = tokenizer.encode(input_context, return_tensors="tf")
        outputs = model.generate(input_ids=input_ids, max_length=50, temperature=0.7, repetition_penalty=1.2)
        print(f"Generated: {tokenizer.decode(outputs[0], skip_special_tokens=True)}")

        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        model = TFAutoModelWithLMHead.from_pretrained("gpt2")
        input_context = "My cute dog"
        bad_words_ids = [
            tokenizer.encode(bad_word, add_prefix_space=True) for bad_word in ["idiot", "stupid", "shut up"]
        ]
        input_ids = tokenizer.encode(input_context, return_tensors="tf")
        
        outputs = model.generate(input_ids=input_ids, max_length=100, do_sample=True, bad_words_ids=bad_words_ids)
        ```"""

        
        self._validate_model_class()
        self._validate_model_kwargs(model_kwargs.copy())

        
        if input_ids is not None:
            if isinstance(input_ids, tf.Tensor) and input_ids.dtype.is_floating:
                pass
            elif isinstance(input_ids, np.ndarray) and np.issubdtype(input_ids.dtype, np.floating):
                pass
            else:
                input_ids = tf.cast(input_ids, tf.int32)
        if attention_mask is not None:
            attention_mask = tf.cast(attention_mask, tf.int32)
        if "decoder_input_ids" in model_kwargs:
            if (
                isinstance(model_kwargs["decoder_input_ids"], tf.Tensor)
                and model_kwargs["decoder_input_ids"].dtype.is_floating
            ):
                pass
            elif isinstance(model_kwargs["decoder_input_ids"], np.ndarray) and np.issubdtype(
                model_kwargs["decoder_input_ids"].dtype, np.floating
            ):
                pass
            else:
                model_kwargs["decoder_input_ids"] = tf.cast(model_kwargs["decoder_input_ids"], tf.int32)

        
        length_penalty = length_penalty if length_penalty is not None else self.config.length_penalty
        early_stopping = early_stopping if early_stopping is not None else self.config.early_stopping

        bos_token_id = bos_token_id if bos_token_id is not None else self.config.bos_token_id
        pad_token_id = pad_token_id if pad_token_id is not None else self.config.pad_token_id
        eos_token_id = eos_token_id if eos_token_id is not None else self.config.eos_token_id

        forced_bos_token_id = (
            forced_bos_token_id if forced_bos_token_id is not None else self.config.forced_bos_token_id
        )
        forced_eos_token_id = (
            forced_eos_token_id if forced_eos_token_id is not None else self.config.forced_eos_token_id
        )

        output_scores = output_scores if output_scores is not None else self.config.output_scores
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict_in_generate = (
            return_dict_in_generate if return_dict_in_generate is not None else self.config.return_dict_in_generate
        )

        num_beams = num_beams if num_beams is not None else self.config.num_beams
        do_sample = do_sample if do_sample is not None else self.config.do_sample
        num_return_sequences = (
            num_return_sequences if num_return_sequences is not None else self.config.num_return_sequences
        )

        if pad_token_id is None and eos_token_id is not None:
            if attention_mask is None:
                logger.warning(
                    "The attention mask and the pad token id were not set. As a consequence, you may observe "
                    "unexpected behavior. Please pass your input's `attention_mask` to obtain reliable results."
                )
            logger.warning(f"Setting `pad_token_id` to {eos_token_id} (first `eos_token_id`) to generate sequence")
            pad_token_id = eos_token_id

        use_xla = not tf.executing_eagerly()
        if use_xla and not self.supports_xla_generation:
            raise ValueError(
                "The selected model does not support Graph mode nor XLA generation (e.g. from tf.function())"
            )

        
        input_ids = self._prepare_model_inputs(input_ids, bos_token_id)
        
        batch_size = shape_list(input_ids)[0]

        
        if output_attentions is not None:
            model_kwargs["output_attentions"] = output_attentions
        if output_hidden_states is not None:
            model_kwargs["output_hidden_states"] = output_hidden_states
        if use_cache is not None:
            model_kwargs["use_cache"] = use_cache
        if attention_mask is not None:
            model_kwargs["attention_mask"] = attention_mask

        accepts_attention_mask = "attention_mask" in set(inspect.signature(self.call).parameters.keys())
        requires_attention_mask = "encoder_outputs" not in model_kwargs

        if model_kwargs.get("attention_mask", None) is None and requires_attention_mask and accepts_attention_mask:
            model_kwargs["attention_mask"] = self._prepare_attention_mask_for_generation(
                input_ids, pad_token_id, eos_token_id
            )

        
        if not self.config.is_encoder_decoder:
            if pad_token_id is not None and tf.math.reduce_any(input_ids[:, -1] == pad_token_id):
                logger.warning(
                    "A decoder-only architecture is being used, but right-padding was detected! For correct "
                    "generation results, please set `padding_side='left'` when initializing the tokenizer."
                )

        
        if self.config.is_encoder_decoder:
            
            model_kwargs = self._prepare_encoder_decoder_kwargs_for_generation(input_ids, model_kwargs)
            
            input_ids = self._prepare_decoder_input_ids_for_generation(
                batch_size,
                decoder_start_token_id=decoder_start_token_id,
                bos_token_id=bos_token_id,
                model_kwargs=model_kwargs,
            )

        
        input_ids_seq_length = input_ids.shape[-1]
        if max_length is None and max_new_tokens is None:
            warnings.warn(
                "Neither `max_length` nor `max_new_tokens` have been set, `max_length` will default to "
                f"{self.config.max_length} (`self.config.max_length`). Controlling `max_length` via the config is "
                "deprecated and `max_length` will be removed from the config in v5 of Transformers -- we recommend "
                "using `max_new_tokens` to control the maximum length of the generation.",
                UserWarning,
            )
        elif max_length is None and max_new_tokens is not None:
            max_length = max_new_tokens + input_ids_seq_length
        elif max_length is not None and max_new_tokens is not None:
            raise ValueError(
                "Both `max_new_tokens` and `max_length` have been set but they serve the same purpose -- setting a"
                " limit to the generated output length. Remove one of those arguments. Please refer to the"
                " documentation for more information. "
                "(https://huggingface.co/docs/transformers/main/en/main_classes/text_generation)"
            )
        
        max_length = max_length if max_length is not None else self.config.max_length
        min_length = min_length if min_length is not None else self.config.min_length

        if min_length is not None and min_length > max_length:
            raise ValueError(
                f"Unfeasable length constraints: the minimum length ({min_length}) is larger than the maximum "
                f"length ({max_length})"
            )
        if input_ids_seq_length >= max_length:
            input_ids_string = "decoder_input_ids" if self.config.is_encoder_decoder else "input_ids"
            logger.warning(
                f"Input length of {input_ids_string} is {input_ids_seq_length}, but `max_length` is set to"
                f" {max_length}. This can lead to unexpected behavior. You should consider increasing"
                "`max_new_tokens`."
            )

        
        
        is_greedy_gen_mode = (num_beams == 1) and do_sample is False
        is_sample_gen_mode = (num_beams == 1) and do_sample is True
        is_beam_gen_mode = (num_beams > 1) and do_sample is False

        
        logits_processor = self._get_logits_processor(
            repetition_penalty=repetition_penalty,
            no_repeat_ngram_size=no_repeat_ngram_size,
            input_ids_seq_length=input_ids_seq_length,
            bad_words_ids=bad_words_ids,
            min_length=min_length,
            max_length=max_length,
            eos_token_id=eos_token_id,
            forced_bos_token_id=forced_bos_token_id,
            forced_eos_token_id=forced_eos_token_id,
            suppress_tokens=suppress_tokens,
            begin_suppress_tokens=begin_suppress_tokens,
            forced_decoder_ids=forced_decoder_ids,
        )

        
        if is_greedy_gen_mode:
            if num_return_sequences > 1:
                raise ValueError(
                    f"num_return_sequences has to be 1, but is {num_return_sequences} when doing greedy search."
                )
            
            return self.greedy_search(
                input_ids,
                max_length=max_length,
                pad_token_id=pad_token_id,
                eos_token_id=eos_token_id,
                logits_processor=logits_processor,
                output_scores=output_scores,
                return_dict_in_generate=return_dict_in_generate,
                **model_kwargs,
            )
        elif is_sample_gen_mode:
            
            logits_warper = self._get_logits_warper(top_k=top_k, top_p=top_p, temperature=temperature)

            
            input_ids, model_kwargs = self._expand_inputs_for_generation(
                input_ids,
                expand_size=num_return_sequences,
                is_encoder_decoder=self.config.is_encoder_decoder,
                **model_kwargs,
            )

            
            return self.sample(
                input_ids,
                logits_processor=logits_processor,
                logits_warper=logits_warper,
                max_length=max_length,
                pad_token_id=pad_token_id,
                eos_token_id=eos_token_id,
                seed=seed,
                output_scores=output_scores,
                return_dict_in_generate=return_dict_in_generate,
                **model_kwargs,
            )

        elif is_beam_gen_mode:
            if num_beams < num_return_sequences:
                raise ValueError(
                    "Greedy beam search decoding cannot return more sequences than it has beams. Please set "
                    f"num_beams >= num_return_sequences, got {num_beams} and {num_return_sequences} (respectivelly)"
                )

            
            input_ids = self._expand_to_num_beams(input_ids, num_beams=num_beams)

            if "encoder_outputs" in model_kwargs:
                model_kwargs["encoder_outputs"]["last_hidden_state"] = self._expand_to_num_beams(
                    model_kwargs["encoder_outputs"]["last_hidden_state"], num_beams=num_beams
                )

            if "attention_mask" in model_kwargs:
                model_kwargs["attention_mask"] = self._expand_to_num_beams(
                    model_kwargs["attention_mask"], num_beams=num_beams
                )

            
            return self.beam_search(
                input_ids,
                max_length=max_length,
                pad_token_id=pad_token_id,
                eos_token_id=eos_token_id,
                length_penalty=length_penalty,
                early_stopping=early_stopping,
                logits_processor=logits_processor,
                return_dict_in_generate=return_dict_in_generate,
                num_return_sequences=num_return_sequences,
                **model_kwargs,
            )

        else:
            
            raise NotImplementedError("Beam sampling is currently not implemented.")

    @staticmethod
    def _expand_to_num_beams(tensor: tf.Tensor, num_beams: int) -> tf.Tensor:
        shape = shape_list(tensor)
        return tf.broadcast_to(tensor[:, None], (shape[0], num_beams) + tuple(shape[1:]))

    def _prepare_attention_mask_for_generation(
        self,
        inputs: tf.Tensor,
        pad_token_id: Optional[int],
        eos_token_id: Optional[int],
    ) -> tf.Tensor:
        is_input_ids = len(inputs.shape) == 2 and inputs.dtype in (tf.int32, tf.int64)
        is_pad_token_in_inputs = (pad_token_id is not None) and tf.math.reduce_any(inputs == pad_token_id)
        is_pad_token_not_equal_to_eos_token_id = (eos_token_id is None) or (pad_token_id != eos_token_id)

        
        if is_input_ids and is_pad_token_in_inputs and is_pad_token_not_equal_to_eos_token_id:
            return tf.cast(tf.math.not_equal(inputs, pad_token_id), dtype=tf.int32)
        else:
            return tf.ones(inputs.shape[:2], dtype=tf.int32)

    def _prepare_encoder_decoder_kwargs_for_generation(self, inputs_tensor: tf.Tensor, model_kwargs) -> Dict[str, Any]:
        
        encoder = self.get_encoder()

        
        irrelevant_prefix = ["decoder_", "cross_attn", "use_cache"]
        encoder_kwargs = {
            argument: value
            for argument, value in model_kwargs.items()
            if not any(argument.startswith(p) for p in irrelevant_prefix)
        }

        
        encoder_kwargs["return_dict"] = True
        encoder_kwargs[self.main_input_name] = inputs_tensor
        encoder_outputs = encoder(**encoder_kwargs)
        model_kwargs["encoder_outputs"] = encoder_outputs

        return model_kwargs

    def _prepare_decoder_input_ids_for_generation(
        self,
        batch_size: int,
        decoder_start_token_id: int = None,
        bos_token_id: int = None,
        model_kwargs: Optional[Dict[str, tf.Tensor]] = None,
    ) -> tf.Tensor:

        
        if model_kwargs is not None and "decoder_input_ids" in model_kwargs:
            return model_kwargs.pop("decoder_input_ids")
        else:
            decoder_start_token_id = self._get_decoder_start_token_id(decoder_start_token_id, bos_token_id)
            return tf.ones((batch_size, 1), dtype=tf.int32) * decoder_start_token_id

    def _get_decoder_start_token_id(self, decoder_start_token_id: int = None, bos_token_id: int = None) -> int:
        
        
        decoder_start_token_id = (
            decoder_start_token_id if decoder_start_token_id is not None else self.config.decoder_start_token_id
        )
        bos_token_id = bos_token_id if bos_token_id is not None else self.config.bos_token_id

        if decoder_start_token_id is not None:
            return decoder_start_token_id
        elif (
            hasattr(self.config, "decoder")
            and hasattr(self.config.decoder, "decoder_start_token_id")
            and self.config.decoder.decoder_start_token_id is not None
        ):
            return self.config.decoder.decoder_start_token_id
        elif bos_token_id is not None:
            return bos_token_id
        elif (
            hasattr(self.config, "decoder")
            and hasattr(self.config.decoder, "bos_token_id")
            and self.config.decoder.bos_token_id is not None
        ):
            return self.config.decoder.bos_token_id
        raise ValueError(
            "`decoder_start_token_id` or `bos_token_id` has to be defined for encoder-decoder generation."
        )

    @staticmethod
    def _expand_inputs_for_generation(
        input_ids: tf.Tensor,
        expand_size: int = 1,
        is_encoder_decoder: bool = False,
        attention_mask: Optional[tf.Tensor] = None,
        encoder_outputs: Optional[ModelOutput] = None,
        **model_kwargs,
    ) -> Tuple[tf.Tensor, Dict[str, Any]]:
        expanded_return_idx = tf.reshape(
            tf.tile(tf.reshape(tf.range(tf.shape(input_ids)[0]), (-1, 1)), (1, expand_size)), (-1,)
        )
        input_ids = tf.gather(input_ids, expanded_return_idx, axis=0)

        if "token_type_ids" in model_kwargs:
            token_type_ids = model_kwargs["token_type_ids"]
            model_kwargs["token_type_ids"] = tf.gather(token_type_ids, expanded_return_idx, axis=0)

        if attention_mask is not None:
            model_kwargs["attention_mask"] = tf.gather(attention_mask, expanded_return_idx, axis=0)

        if is_encoder_decoder:
            if encoder_outputs is None:
                raise ValueError("If `is_encoder_decoder` is True, make sure that `encoder_outputs` is defined.")
            encoder_outputs["last_hidden_state"] = tf.gather(
                encoder_outputs.last_hidden_state, expanded_return_idx, axis=0
            )
            model_kwargs["encoder_outputs"] = encoder_outputs
        return input_ids, model_kwargs

    def _prepare_model_inputs(self, inputs: Optional[tf.Tensor] = None, bos_token_id: Optional[int] = None):
        
        
        if inputs is None:
            
            if not isinstance(bos_token_id, int) or bos_token_id < 0:
                raise ValueError(
                    "you should either supply a context to complete as `input_ids` input "
                    "or a `bos_token_id` (integer >= 0) as a first token to start the generation."
                )
            return tf.cast(tf.fill((1, 1), bos_token_id), dtype=tf.int32)

        return inputs

    @staticmethod
    def _update_model_kwargs_for_generation(
        outputs: ModelOutput, model_kwargs: Dict[str, Any], is_encoder_decoder: bool = False
    ) -> Dict[str, Any]:
        
        if "past_key_values" in outputs:
            model_kwargs["past"] = outputs.past_key_values
        elif "mems" in outputs:
            model_kwargs["past"] = outputs.mems
        elif "past_buckets_states" in outputs:
            model_kwargs["past"] = outputs.past_buckets_states
        else:
            model_kwargs["past"] = None

        
        if not is_encoder_decoder:
            if "attention_mask" in model_kwargs:
                attention_mask = model_kwargs["attention_mask"]
                model_kwargs["attention_mask"] = tf.concat(
                    [attention_mask, tf.ones((shape_list(attention_mask)[0], 1), dtype=tf.int32)], axis=-1
                )

        return model_kwargs

    def _update_model_kwargs_for_xla_generation(
        self,
        model_outputs: ModelOutput,
        model_kwargs: Dict[str, Any],
        cur_len: int,
        max_length: int,
        batch_size: int,
        is_encoder_decoder: bool = False,
        batch_axis: int = 0,
    ):
        def _initialize_attention(model_kwargs, num_padding_values, is_encoder_decoder):
            """initializes the appropriate attention mask -- encoder-decoder models use `decoder_attention_mask`"""
            if is_encoder_decoder:
                
                
                decoder_attention_mask = tf.concat(
                    [
                        tf.ones((batch_size, 1), dtype=tf.int32),
                        tf.zeros((batch_size, num_padding_values), dtype=tf.int32),
                        tf.ones((batch_size, 1), dtype=tf.int32),
                    ],
                    axis=1,
                )
                mask = {"decoder_attention_mask": decoder_attention_mask}
            else:
                attention_mask = model_kwargs.pop("attention_mask")
                
                attention_mask = tf.concat(
                    [
                        attention_mask,
                        tf.zeros((batch_size, num_padding_values), dtype=attention_mask.dtype),
                        tf.ones((batch_size, 1), dtype=attention_mask.dtype),
                    ],
                    axis=1,
                )
                mask = {"attention_mask": attention_mask}
            return mask

        def _update_attention(model_kwargs, new_past_index, is_encoder_decoder):
            """updates the appropriate attention mask -- encoder-decoder models use `decoder_attention_mask`"""
            update_start = tf.constant([0, 1], dtype=tf.int32) * new_past_index
            if is_encoder_decoder:
                decoder_attention_mask = model_kwargs.pop("decoder_attention_mask")
                decoder_attention_mask_update_slice = tf.ones((batch_size, 1), dtype=decoder_attention_mask.dtype)
                decoder_attention_mask = dynamic_update_slice(
                    decoder_attention_mask, decoder_attention_mask_update_slice, update_start
                )
                mask = {"decoder_attention_mask": decoder_attention_mask}
            else:
                attention_mask = model_kwargs.pop("attention_mask")
                attention_mask_update_slice = tf.ones((batch_size, 1), dtype=attention_mask.dtype)
                attention_mask = dynamic_update_slice(attention_mask, attention_mask_update_slice, update_start)
                mask = {"attention_mask": attention_mask}
            return mask

        def _initialize_past(past, num_padding_values, batch_axis):
            """initialize past with zeros -- the structure depends on `batch_axis`"""
            if batch_axis == 0:
                padding_values = tf.constant([[0, 0], [0, 0], [0, num_padding_values], [0, 0]], dtype=tf.int32)
                new_past = ()
                for past_layer in past:
                    new_past_layer = list(past_layer)
                    for i in range(len(new_past_layer[:2])):
                        new_past_layer[i] = tf.pad(past_layer[i], padding_values)
                    new_past += (tuple(new_past_layer),)
            else:
                padding_values = tf.scatter_nd(indices=[[3, 1]], updates=[num_padding_values], shape=(5, 2))
                new_past = list(past)
                for i in range(len(past)):
                    new_past[i] = tf.pad(past[i], padding_values)
            return new_past

        def _update_past(past, new_past_index, batch_axis):
            if batch_axis == 0:
                slice_start_base = tf.constant([0, 0, 1, 0])
                new_past = ()
                for past_layer in past:
                    new_past_layer = list(past_layer)
                    for i in range(len(new_past_layer[:2])):
                        update_slice = past_layer[i][:, :, -1:]
                        
                        
                        new_past_layer[i] = dynamic_update_slice(
                            past_layer[i][:, :, :-1], update_slice, slice_start_base * new_past_index
                        )
                    new_past += (tuple(new_past_layer),)
            else:
                slice_start_base = tf.constant([0, 0, 0, 1, 0])
                new_past = [None for _ in range(len(past))]
                for i in range(len(past)):
                    update_slice = past[i][:, :, :, -1:]
                    
                    
                    new_past[i] = dynamic_update_slice(
                        past[i][:, :, :, :-1], update_slice, slice_start_base * new_past_index
                    )
            return new_past

        if "past_key_values" in model_outputs:
            past = model_outputs.past_key_values
        elif "mems" in model_outputs:
            past = model_outputs.mems
        elif "past_buckets_states" in model_outputs:
            past = model_outputs.past_buckets_states
        else:
            raise ValueError(
                f"No known past variable found in model outputs (model outputs keys: {list(model_outputs.keys())})"
            )
        is_past_initialized = model_kwargs.pop("past", None) is not None

        if not is_past_initialized:
            
            
            
            num_padding_values = max_length - cur_len - 1
            mask = _initialize_attention(model_kwargs, num_padding_values, is_encoder_decoder)
            new_past = _initialize_past(past, num_padding_values, batch_axis)
        else:
            
            
            
            new_past_index = cur_len - 2
            mask = _update_attention(model_kwargs, new_past_index, is_encoder_decoder)
            new_past = _update_past(past, new_past_index, batch_axis)

        
        model_kwargs.update(mask)
        model_kwargs["past"] = tuple(new_past)

        return model_kwargs

    def _get_logits_warper(
        self,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        temperature: Optional[float] = None,
    ) -> TFLogitsProcessorList:
        """
        This class returns a [`TFLogitsProcessorList`] list object that contains all relevant [`TFLogitsWarper`]
        instances used for multinomial sampling.
        """

        
        top_k = top_k if top_k is not None else self.config.top_k
        top_p = top_p if top_p is not None else self.config.top_p
        temperature = temperature if temperature is not None else self.config.temperature
        
        warpers = TFLogitsProcessorList()

        
        
        if temperature is not None and temperature != 1.0:
            warpers.append(TFTemperatureLogitsWarper(temperature))
        if top_k is not None and top_k != 0:
            warpers.append(TFTopKLogitsWarper(top_k=top_k, min_tokens_to_keep=1))
        if top_p is not None and top_p < 1.0:
            warpers.append(TFTopPLogitsWarper(top_p=top_p, min_tokens_to_keep=1))
        return warpers

    def _get_logits_processor(
        self,
        repetition_penalty: float,
        no_repeat_ngram_size: int,
        input_ids_seq_length: int,
        bad_words_ids: List[List[int]],
        min_length: int,
        max_length: int,
        eos_token_id: int,
        forced_bos_token_id: int,
        forced_eos_token_id: int,
        suppress_tokens: Optional[List[int]] = None,
        begin_suppress_tokens: Optional[List[int]] = None,
        forced_decoder_ids: Optional[List[List[int]]] = None,
    ) -> TFLogitsProcessorList:
        """
        This class returns a [`TFLogitsProcessorList`] list object that contains all relevant [`TFLogitsProcessor`]
        instances used to modify the scores of the language model head.
        """
        processors = TFLogitsProcessorList()

        repetition_penalty = repetition_penalty if repetition_penalty is not None else self.config.repetition_penalty
        no_repeat_ngram_size = (
            no_repeat_ngram_size if no_repeat_ngram_size is not None else self.config.no_repeat_ngram_size
        )
        bad_words_ids = bad_words_ids if bad_words_ids is not None else self.config.bad_words_ids
        eos_token_id = eos_token_id if eos_token_id is not None else self.config.eos_token_id
        suppress_tokens = suppress_tokens if suppress_tokens is not None else self.config.suppress_tokens
        begin_suppress_tokens = (
            begin_suppress_tokens if begin_suppress_tokens is not None else self.config.begin_suppress_tokens
        )
        if forced_decoder_ids is None and hasattr(self.config, "forced_decoder_ids"):
            forced_decoder_ids = self.config.forced_decoder_ids

        
        if repetition_penalty is not None and repetition_penalty != 1.0:
            processors.append(TFRepetitionPenaltyLogitsProcessor(penalty=repetition_penalty))
        if no_repeat_ngram_size is not None and no_repeat_ngram_size > 0:
            processors.append(TFNoRepeatNGramLogitsProcessor(no_repeat_ngram_size))
        if bad_words_ids is not None:
            processors.append(TFNoBadWordsLogitsProcessor(bad_words_ids, eos_token_id))
        if min_length is not None and eos_token_id is not None and min_length > 0:
            processors.append(TFMinLengthLogitsProcessor(min_length, eos_token_id))
        if forced_bos_token_id is not None:
            processors.append(TFForcedBOSTokenLogitsProcessor(forced_bos_token_id))
        if forced_eos_token_id is not None:
            processors.append(TFForcedEOSTokenLogitsProcessor(max_length, forced_eos_token_id))
        if suppress_tokens is not None:
            processors.append(TFSuppressTokensLogitsProcessor(suppress_tokens))
        if begin_suppress_tokens is not None:
            begin_index = input_ids_seq_length
            begin_index = begin_index if (input_ids_seq_length > 1 or forced_bos_token_id is None) else begin_index + 1
            if forced_decoder_ids is not None:
                begin_index += forced_decoder_ids[-1][0]  
            processors.append(TFSuppressTokensAtBeginLogitsProcessor(begin_suppress_tokens, begin_index))
        if forced_decoder_ids is not None:
            processors.append(TFForceTokensLogitsProcessor(forced_decoder_ids))
        return processors

    def greedy_search(
        self,
        input_ids: tf.Tensor,
        max_length: Optional[int] = None,
        pad_token_id: Optional[int] = None,
        eos_token_id: Optional[int] = None,
        logits_processor: Optional[TFLogitsProcessorList] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        output_scores: Optional[bool] = None,
        return_dict_in_generate: Optional[bool] = None,
        **model_kwargs,
    ) -> Union[TFGreedySearchOutput, tf.Tensor]:
        r"""
        Generates sequences for models with a language modeling head using greedy decoding.

        Parameters:
            input_ids (`tf.Tensor` of shape `(batch_size, sequence_length)`):
                The sequence used as a prompt for the generation.
            logits_processor (`TFLogitsProcessorList`, *optional*):
                An instance of [`TFLogitsProcessorList`]. List of instances of class derived from [`TFLogitsProcessor`]
                used to modify the prediction scores of the language modeling head applied at each generation step.
            max_length (`int`, *optional*, defaults to 20):
                The maximum length of the sequence to be generated.
            pad_token_id (`int`, *optional*):
                The id of the *padding* token.
            eos_token_id (`int`, *optional*):
                The id of the *end-of-sequence* token.
            output_attentions (`bool`, *optional*, defaults to `False`):
                Whether or not to return the attentions tensors of all attention layers. See `attentions` under
                returned tensors for more details.
            output_hidden_states (`bool`, *optional*, defaults to `False`):
                Whether or not to return the hidden states of all layers. See `hidden_states` under returned tensors
                for more details.
            output_scores (`bool`, *optional*, defaults to `False`):
                Whether or not to return the prediction scores. See `scores` under returned tensors for more details.
            return_dict_in_generate (`bool`, *optional*, defaults to `False`):
                Whether or not to return a [`~utils.ModelOutput`] instead of a plain tuple.
            model_kwargs:
                Additional model specific keyword arguments will be forwarded to the `call` function of the model. If
                model is an encoder-decoder model the kwargs should include `encoder_outputs`.

        Return:
            [`~generation_tf_utils.TFGreedySearchDecoderOnlyOutput`],
            [`~generation_tf_utils.TFGreedySearchEncoderDecoderOutput`] or `tf.Tensor`: A `tf.Tensor` containing the
            generated tokens (default behaviour) or a [`~generation_tf_utils.TFGreedySearchDecoderOnlyOutput`] if
            `model.config.is_encoder_decoder=False` and `return_dict_in_generate=True` or a
            [`~generation_tf_utils.TFGreedySearchEncoderDecoderOutput`] if `model.config.is_encoder_decoder=True`.

        Examples:

        ```python
        >>> from transformers import (
        ...     AutoTokenizer,
        ...     TFAutoModelForCausalLM,
        ...     TFLogitsProcessorList,
        ...     TFMinLengthLogitsProcessor,
        ... )

        >>> tokenizer = AutoTokenizer.from_pretrained("gpt2")
        >>> model = TFAutoModelForCausalLM.from_pretrained("gpt2")

        >>> 
        >>> model.config.pad_token_id = model.config.eos_token_id

        >>> input_prompt = "Today is a beautiful day, and"
        >>> input_ids = tokenizer(input_prompt, return_tensors="tf").input_ids

        >>> 
        >>> logits_processor = TFLogitsProcessorList(
        ...     [
        ...         TFMinLengthLogitsProcessor(15, eos_token_id=model.config.eos_token_id),
        ...     ]
        ... )

        >>> outputs = model.greedy_search(input_ids, logits_processor=logits_processor)

        >>> print("Generated:", tokenizer.batch_decode(outputs, skip_special_tokens=True))
        ```"""

        
        logits_processor = logits_processor if logits_processor is not None else TFLogitsProcessorList()

        max_length = max_length if max_length is not None else self.config.max_length
        pad_token_id = pad_token_id if pad_token_id is not None else self.config.pad_token_id
        eos_token_id = eos_token_id if eos_token_id is not None else self.config.eos_token_id
        output_scores = output_scores if output_scores is not None else self.config.output_scores
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict_in_generate = (
            return_dict_in_generate if return_dict_in_generate is not None else self.config.return_dict_in_generate
        )
        use_xla = not tf.executing_eagerly()
        
        
        model_name = str(self.decoder) if "EncoderDecoder" in str(self) else str(self)
        cache_batch_axis = 1 if any([model_prefix in model_name for model_prefix in ("TFGPT2", "TFCTRL")]) else 0
        
        needs_full_input = "use_mems" in set(inspect.signature(self.prepare_inputs_for_generation).parameters.keys())

        
        scores = [] if (return_dict_in_generate and output_scores) else None
        decoder_attentions = [] if (return_dict_in_generate and output_attentions) else None
        cross_attentions = [] if (return_dict_in_generate and output_attentions) else None
        decoder_hidden_states = [] if (return_dict_in_generate and output_hidden_states) else None

        "xla-compileable" generate function
        batch_size, cur_len = shape_list(input_ids)

        
        input_ids_padding = tf.ones((batch_size, max_length - cur_len), dtype=tf.int32) * (pad_token_id or 0)
        generated = tf.concat([input_ids, input_ids_padding], axis=-1)
        finished_sequences = tf.zeros((batch_size,), dtype=tf.bool)

        "xla-compile-able" stop-condition and auto-regressive function
        
        def greedy_search_cond_fn(generated, finished_sequences, cur_len, model_kwargs):
            """state termination condition fn."""
            return ~tf.reduce_all(finished_sequences)

        
        def greedy_search_body_fn(generated, finished_sequences, cur_len, model_kwargs):
            """state update fn."""
            if model_kwargs.get("past") is None or needs_full_input:
                input_ids = generated[:, :cur_len]
            else:
                input_ids = tf.expand_dims(generated[:, cur_len - 1], -1)
            model_inputs = self.prepare_inputs_for_generation(input_ids, **model_kwargs)
            
            model_outputs = self(
                **model_inputs,
                return_dict=True,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
            )
            next_token_logits = model_outputs.logits[:, -1]

            
            if not use_xla and return_dict_in_generate:
                if output_scores:
                    scores.append(next_token_logits)
                if output_attentions and self.config.is_encoder_decoder:
                    decoder_attentions.append(model_outputs.decoder_attentions)
                elif output_attentions and not self.config.is_encoder_decoder:
                    decoder_attentions.append(model_outputs.attentions)
                    if self.config.is_encoder_decoder:
                        cross_attentions.append(model_outputs.cross_attentions)

                if output_hidden_states and self.config.is_encoder_decoder:
                    decoder_hidden_states.append(model_outputs.decoder_hidden_states)
                elif output_hidden_states and self.config.is_encoder_decoder:
                    decoder_hidden_states.append(model_outputs.hidden_states)

            
            next_tokens_scores = logits_processor(generated, next_token_logits, cur_len)

            
            next_tokens = tf.argmax(next_tokens_scores, axis=-1, output_type=tf.int32)

            if eos_token_id is not None:
                if pad_token_id is None:
                    raise ValueError("If `eos_token_id` is defined, make sure that `pad_token_id` is defined.")
                unfinished_seq = 1 - tf.cast(finished_sequences, tf.int32)
                next_tokens = next_tokens * unfinished_seq + pad_token_id * (1 - unfinished_seq)
            finished_sequences = finished_sequences | (next_tokens == eos_token_id)

            
            update_indices = tf.stack([tf.range(batch_size), tf.broadcast_to(cur_len, [batch_size])], axis=-1)
            generated = tf.tensor_scatter_nd_update(tensor=generated, indices=update_indices, updates=next_tokens)
            cur_len += 1

            
            if use_xla:
                model_kwargs = self._update_model_kwargs_for_xla_generation(
                    model_outputs=model_outputs,
                    model_kwargs=model_kwargs,
                    cur_len=cur_len,
                    max_length=max_length,
                    batch_size=batch_size,
                    is_encoder_decoder=self.config.is_encoder_decoder,
                    batch_axis=cache_batch_axis,
                )
            else:
                model_kwargs = self._update_model_kwargs_for_generation(
                    model_outputs, model_kwargs, is_encoder_decoder=self.config.is_encoder_decoder
                )
                
                if model_kwargs.get("past", None) is None:
                    
                    model_kwargs.pop("past", None)

            return generated, finished_sequences, cur_len, model_kwargs

        
        
        generated, finished_sequences, cur_len, model_kwargs = greedy_search_body_fn(
            generated, finished_sequences, cur_len, model_kwargs
        )

        
        
        if greedy_search_cond_fn(generated, finished_sequences, cur_len, model_kwargs):
            maximum_iterations = max_length - cur_len
            generated, _, cur_len, _ = tf.while_loop(
                greedy_search_cond_fn,
                greedy_search_body_fn,
                (generated, finished_sequences, cur_len, model_kwargs),
                maximum_iterations=maximum_iterations,
            )

        
        if not use_xla:
            
            generated = generated[:, :cur_len]

        if return_dict_in_generate:
            if self.config.is_encoder_decoder:
                
                
                encoder_attentions = model_kwargs["encoder_outputs"].get("attentions") if output_attentions else None
                encoder_hidden_states = (
                    model_kwargs["encoder_outputs"].get("hidden_states") if output_hidden_states else None
                )

                scores = tuple(scores) if scores is not None else None
                decoder_attentions = tuple(decoder_attentions) if decoder_attentions is not None else None
                cross_attentions = tuple(cross_attentions) if cross_attentions is not None else None
                decoder_hidden_states = tuple(decoder_hidden_states) if decoder_hidden_states is not None else None

                return TFGreedySearchEncoderDecoderOutput(
                    sequences=generated,
                    scores=scores,
                    encoder_attentions=encoder_attentions,
                    encoder_hidden_states=encoder_hidden_states,
                    decoder_attentions=decoder_attentions,
                    cross_attentions=cross_attentions,
                    decoder_hidden_states=decoder_hidden_states,
                )
            else:
                return TFGreedySearchDecoderOnlyOutput(
                    sequences=generated,
                    scores=scores,
                    attentions=decoder_attentions,
                    hidden_states=decoder_hidden_states,
                )
        else:
            return generated

    def sample(
        self,
        input_ids: tf.Tensor,
        logits_processor: Optional[TFLogitsProcessorList] = None,
        logits_warper: Optional[TFLogitsProcessorList] = None,
        max_length: Optional[int] = None,
        pad_token_id: Optional[int] = None,
        eos_token_id: Optional[int] = None,
        seed: Optional[Tuple[int, int]] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        output_scores: Optional[bool] = None,
        return_dict_in_generate: Optional[bool] = None,
        **model_kwargs,
    ) -> Union[TFSampleOutput, tf.Tensor]:
        r"""
        Generates sequences for models with a language modeling head using multinomial sampling.

        Parameters:
            input_ids (`tf.Tensor` of shape `(batch_size, sequence_length)`):
                The sequence used as a prompt for the generation.
            logits_processor (`TFLogitsProcessorList`, *optional*):
                An instance of [`TFLogitsProcessorList`]. List of instances of class derived from [`TFLogitsProcessor`]
                used to modify the prediction scores of the language modeling head applied at each generation step.
            logits_warper (`TFLogitsProcessorList`, *optional*):
                An instance of [`TFLogitsProcessorList`]. List of instances of class derived from [`TFLogitsWarper`]
                used to warp the prediction score distribution of the language modeling head applied before multinomial
                sampling at each generation step.
            max_length (`int`, *optional*, defaults to 20):
                The maximum length of the sequence to be generated.
            pad_token_id (`int`, *optional*):
                The id of the *padding* token.
            eos_token_id (`int`, *optional*):
                The id of the *end-of-sequence* token.
            seed (`List[int]`, *optional*):
                Random seed to control sampling, containing two integers, used when `do_sample` is `True`. See the
                `seed` argument from stateless functions in `tf.random`.
            output_attentions (`bool`, *optional*, defaults to `False`):
                Whether or not to return the attentions tensors of all attention layers. See `attentions` under
                returned tensors for more details.
            output_hidden_states (`bool`, *optional*, defaults to `False`):
                Whether or not to return the hidden states of all layers. See `hidden_states` under returned tensors
                for more details.
            output_scores (`bool`, *optional*, defaults to `False`):
                Whether or not to return the prediction scores. See `scores` under returned tensors for more details.
            return_dict_in_generate (`bool`, *optional*, defaults to `False`):
                Whether or not to return a [`~utils.ModelOutput`] instead of a plain tuple.
            model_kwargs:
                Additional model specific kwargs will be forwarded to the `call` function of the model. If model is an
                encoder-decoder model the kwargs should include `encoder_outputs`.

        Return:
            [`~generation_tf_utils.TFSampleDecoderOnlyOutput`], [`~generation_tf_utils.TFSampleEncoderDecoderOutput`]
            or `tf.Tensor`: A `tf.Tensor` containing the generated tokens (default behaviour) or a
            [`~generation_tf_utils.TFSampleDecoderOnlyOutput`] if `model.config.is_encoder_decoder=False` and
            `return_dict_in_generate=True` or a [`~generation_tf_utils.TFSampleEncoderDecoderOutput`] if
            `model.config.is_encoder_decoder=True`.

        Examples:

        ```python
        >>> from transformers import (
        ...     AutoTokenizer,
        ...     TFAutoModelForCausalLM,
        ...     TFLogitsProcessorList,
        ...     TFMinLengthLogitsProcessor,
        ...     TFTopKLogitsWarper,
        ...     TFTemperatureLogitsWarper,
        ... )

        >>> tokenizer = AutoTokenizer.from_pretrained("gpt2")
        >>> model = TFAutoModelForCausalLM.from_pretrained("gpt2")

        >>> 
        >>> model.config.pad_token_id = model.config.eos_token_id

        >>> input_prompt = "Today is a beautiful day, and"
        >>> input_ids = tokenizer(input_prompt, return_tensors="tf").input_ids

        >>> 
        >>> logits_processor = TFLogitsProcessorList(
        ...     [
        ...         TFMinLengthLogitsProcessor(15, eos_token_id=model.config.eos_token_id),
        ...     ]
        ... )
        >>> 
        >>> logits_warper = TFLogitsProcessorList(
        ...     [
        ...         TFTopKLogitsWarper(50),
        ...         TFTemperatureLogitsWarper(0.7),
        ...     ]
        ... )

        >>> outputs = model.sample(input_ids, logits_processor=logits_processor, logits_warper=logits_warper)

        >>> print("Generated:", tokenizer.batch_decode(outputs, skip_special_tokens=True))
        ```"""

        
        logits_processor = logits_processor if logits_processor is not None else TFLogitsProcessorList()
        logits_warper = logits_warper if logits_warper is not None else TFLogitsProcessorList()

        max_length = max_length if max_length is not None else self.config.max_length
        pad_token_id = pad_token_id if pad_token_id is not None else self.config.pad_token_id
        eos_token_id = eos_token_id if eos_token_id is not None else self.config.eos_token_id
        output_scores = output_scores if output_scores is not None else self.config.output_scores
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict_in_generate = (
            return_dict_in_generate if return_dict_in_generate is not None else self.config.return_dict_in_generate
        )
        use_xla = not tf.executing_eagerly()
        
        
        model_name = str(self.decoder) if "EncoderDecoder" in str(self) else str(self)
        cache_batch_axis = 1 if any([model_prefix in model_name for model_prefix in ("TFGPT2", "TFCTRL")]) else 0
        
        needs_full_input = "use_mems" in set(inspect.signature(self.prepare_inputs_for_generation).parameters.keys())

        
        scores = [] if (return_dict_in_generate and output_scores) else None
        decoder_attentions = [] if (return_dict_in_generate and output_attentions) else None
        cross_attentions = [] if (return_dict_in_generate and output_attentions) else None
        decoder_hidden_states = [] if (return_dict_in_generate and output_hidden_states) else None

        "xla-compileable" generate function
        batch_size, cur_len = shape_list(input_ids)

        
        input_ids_padding = tf.ones((batch_size, max_length - cur_len), dtype=tf.int32) * (pad_token_id or 0)
        generated = tf.concat([input_ids, input_ids_padding], axis=-1)
        finished_sequences = tf.zeros((batch_size,), dtype=tf.bool)

        "xla-compile-able" stop-condition and auto-regressive function
        def sample_cond_fn(generated, finished_sequences, cur_len, model_kwargs):
            return ~tf.reduce_all(finished_sequences)

        def sample_body_fn(generated, finished_sequences, cur_len, model_kwargs):
            if model_kwargs.get("past") is None or needs_full_input:
                input_ids = generated[:, :cur_len]
            else:
                input_ids = tf.expand_dims(generated[:, cur_len - 1], -1)
            model_inputs = self.prepare_inputs_for_generation(input_ids, **model_kwargs)
            
            model_outputs = self(
                **model_inputs,
                return_dict=True,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
            )
            next_token_logits = model_outputs.logits[:, -1]

            
            if not use_xla and return_dict_in_generate:
                if output_scores:
                    scores.append(next_token_logits)
                if output_attentions and self.config.is_encoder_decoder:
                    decoder_attentions.append(model_outputs.decoder_attentions)
                elif output_attentions and not self.config.is_encoder_decoder:
                    decoder_attentions.append(model_outputs.attentions)
                    if self.config.is_encoder_decoder:
                        cross_attentions.append(model_outputs.cross_attentions)

                if output_hidden_states and self.config.is_encoder_decoder:
                    decoder_hidden_states.append(model_outputs.decoder_hidden_states)
                elif output_hidden_states and self.config.is_encoder_decoder:
                    decoder_hidden_states.append(model_outputs.hidden_states)

            
            next_tokens_scores = logits_processor(generated, next_token_logits, cur_len)
            next_tokens_scores = logits_warper(generated, next_tokens_scores, cur_len)

            
            if seed is not None:
                sample_seed = seed
            else:
                sample_seed = tf.experimental.numpy.random.randint(tf.int32.min, tf.int32.max, (2,), dtype=tf.int32)
            next_tokens = tf.squeeze(
                tf.random.stateless_categorical(
                    logits=next_tokens_scores, num_samples=1, seed=sample_seed, dtype=tf.int32
                ),
                axis=1,
            )

            if eos_token_id is not None:
                if pad_token_id is None:
                    raise ValueError("If `eos_token_id` is defined, make sure that `pad_token_id` is defined.")
                unfinished_seq = 1 - tf.cast(finished_sequences, tf.int32)
                next_tokens = next_tokens * unfinished_seq + pad_token_id * (1 - unfinished_seq)
            finished_sequences = finished_sequences | (next_tokens == eos_token_id)

            
            update_indices = tf.stack([tf.range(batch_size), tf.broadcast_to(cur_len, [batch_size])], axis=-1)
            generated = tf.tensor_scatter_nd_update(tensor=generated, indices=update_indices, updates=next_tokens)
            cur_len += 1

            
            if use_xla:
                model_kwargs = self._update_model_kwargs_for_xla_generation(
                    model_outputs=model_outputs,
                    model_kwargs=model_kwargs,
                    cur_len=cur_len,
                    max_length=max_length,
                    batch_size=batch_size,
                    is_encoder_decoder=self.config.is_encoder_decoder,
                    batch_axis=cache_batch_axis,
                )
            else:
                model_kwargs = self._update_model_kwargs_for_generation(
                    model_outputs, model_kwargs, is_encoder_decoder=self.config.is_encoder_decoder
                )
                
                if model_kwargs.get("past", None) is None:
                    
                    model_kwargs.pop("past", None)

            return generated, finished_sequences, cur_len, model_kwargs

        
        
        generated, finished_sequences, cur_len, model_kwargs = sample_body_fn(
            generated, finished_sequences, cur_len, model_kwargs
        )

        
        
        if sample_cond_fn(generated, finished_sequences, cur_len, model_kwargs):
            maximum_iterations = max_length - cur_len
            generated, _, cur_len, _ = tf.while_loop(
                sample_cond_fn,
                sample_body_fn,
                (generated, finished_sequences, cur_len, model_kwargs),
                maximum_iterations=maximum_iterations,
            )

        
        if not use_xla:
            
            generated = generated[:, :cur_len]

        if return_dict_in_generate:
            if self.config.is_encoder_decoder:
                
                
                encoder_attentions = model_kwargs["encoder_outputs"].get("attentions") if output_attentions else None
                encoder_hidden_states = (
                    model_kwargs["encoder_outputs"].get("hidden_states") if output_hidden_states else None
                )

                scores = tuple(scores) if scores is not None else None
                decoder_attentions = tuple(decoder_attentions) if decoder_attentions is not None else None
                cross_attentions = tuple(cross_attentions) if cross_attentions is not None else None
                decoder_hidden_states = tuple(decoder_hidden_states) if decoder_hidden_states is not None else None

                return TFSampleEncoderDecoderOutput(
                    sequences=generated,
                    scores=scores,
                    encoder_attentions=encoder_attentions,
                    encoder_hidden_states=encoder_hidden_states,
                    decoder_attentions=decoder_attentions,
                    cross_attentions=cross_attentions,
                    decoder_hidden_states=decoder_hidden_states,
                )
            else:
                return TFSampleDecoderOnlyOutput(
                    sequences=generated,
                    scores=scores,
                    attentions=decoder_attentions,
                    hidden_states=decoder_hidden_states,
                )
        else:
            return generated

    def beam_search(
        self,
        input_ids: tf.Tensor,
        max_length: Optional[int] = None,
        pad_token_id: Optional[int] = None,
        eos_token_id: Optional[int] = None,
        length_penalty: Optional[float] = None,
        early_stopping: Optional[bool] = None,
        logits_processor: Optional[TFLogitsProcessorList] = None,
        num_return_sequences: Optional[int] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        output_scores: Optional[bool] = None,
        return_dict_in_generate: Optional[bool] = None,
        **model_kwargs,
    ) -> Union[TFBeamSearchOutput, tf.Tensor]:
        r"""
        Generates sequences for models with a language modeling head using beam search with multinomial sampling.

        Parameters:
            input_ids (`tf.Tensor` of shape `(batch_size, sequence_length)`):
                The sequence used as a prompt for the generation.
            max_length (`int`, *optional*, defaults to 20):
                The maximum length of the sequence to be generated.
            pad_token_id (`int`, *optional*):
                The id of the *padding* token.
            eos_token_id (`int`, *optional*):
                The id of the *end-of-sequence* token.
            length_penalty (`float`, *optional*, defaults to 1.0):
                Exponential penalty to the length that is used with beam-based generation. It is applied as an exponent
                to the sequence length, which in turn is used to divide the score of the sequence. Since the score is
                the log likelihood of the sequence (i.e. negative), `length_penalty` > 0.0 promotes longer sequences,
                while `length_penalty` < 0.0 encourages shorter sequences.
            early_stopping (`bool`, *optional*, defaults to `False`):
                Whether to stop the beam search when at least `num_beams` sentences are finished per batch or not.
            logits_processor (`[TFLogitsProcessorList]`, *optional*):
                An instance of [`TFLogitsProcessorList`]. List of instances of class derived from [`TFLogitsProcessor`]
                used to modify the prediction scores of the language modeling head applied at each generation step.
            num_return_sequences(`int`, *optional*, defaults to 1):
                The number of independently computed returned sequences for each element in the batch.
            output_attentions (`bool`, *optional*, defaults to `False`):
                Whether or not to return the attentions tensors of all attention layers. See `attentions` under
                returned tensors for more details.
            output_hidden_states (`bool`, *optional*, defaults to `False`):
                Whether or not to return the hidden states of all layers. See `hidden_states` under returned tensors
                for more details.
            return_dict_in_generate (`bool`, *optional*, defaults to `False`):
                Whether or not to return a [`~file_utils.ModelOutput`] instead of a plain tuple.
            model_kwargs:
                Additional model specific kwargs will be forwarded to the `call` function of the model. If model is an
                encoder-decoder model the kwargs should include `encoder_outputs`.

        Return:
            [`~generation_tf_utils.TFBeamSearchDecoderOnlyOutput`],
            [`~generation_tf_utils.TFBeamSearchEncoderDecoderOutput`] or `tf.Tensor`: A `tf.Tensor` containing the
            generated tokens (default behaviour) or a [`~generation_tf_utils.TFBeamSearchDecoderOnlyOutput`] if
            `model.config.is_encoder_decoder=False` and `return_dict_in_generate=True` or a
            [`~generation_tf_utils.TFBeamSearchEncoderDecoderOutput`] if `model.config.is_encoder_decoder=True`.

        Examples:

        ```python
        >>> from transformers import (
        ...     AutoTokenizer,
        ...     TFAutoModelForSeq2SeqLM,
        ...     TFLogitsProcessorList,
        ...     TFMinLengthLogitsProcessor,
        ... )
        >>> import tensorflow as tf

        >>> tokenizer = AutoTokenizer.from_pretrained("t5-base")
        >>> model = TFAutoModelForSeq2SeqLM.from_pretrained("t5-base")

        >>> encoder_input_str = "translate English to German: How old are you?"
        >>> encoder_input_ids = tokenizer(encoder_input_str, return_tensors="tf").input_ids

        >>> 
        >>> num_beams = 3
        >>> 
        >>> input_ids = tf.ones((num_beams, 1), dtype=tf.int64)
        >>> input_ids = input_ids * model.config.decoder_start_token_id

        >>> 
        >>> model_kwargs = {
        ...     "encoder_outputs": model.get_encoder()(
        ...         tf.repeat(encoder_input_ids, num_beams, axis=0), return_dict=True
        ...     )
        ... }

        >>> 
        >>> logits_processor = TFLogitsProcessorList(
        ...     [TFMinLengthLogitsProcessor(5, eos_token_id=model.config.eos_token_id)]
        ... )

        >>> outputs = model.beam_search(input_ids, logits_processor=logits_processor, **model_kwargs)

        >>> print("Generated:", tokenizer.batch_decode(outputs, skip_special_tokens=True))
        ```"""

        def flatten_beam_dim(tensor, batch_axis=0):
            """Flattens the first two dimensions of a non-scalar array."""
            shape = shape_list(tensor)
            return tf.reshape(
                tensor,
                shape[:batch_axis] + [shape[batch_axis] * shape[batch_axis + 1]] + shape[batch_axis + 2 :],
            )

        def unflatten_beam_dim(tensor, batch_size, num_beams, batch_axis=0):
            """Unflattens the first, flat batch*beam dimension of a non-scalar array."""
            shape = shape_list(tensor)
            return tf.reshape(tensor, shape[:batch_axis] + [batch_size, num_beams] + shape[batch_axis + 1 :])

        def gather_beams(nested, beam_indices, batch_axis=0):
            """Gathers the beam slices indexed by beam_indices into new beam array."""

            def gather_fn(tensor):
                if batch_axis > 0:
                    
                    perm = tf.concat((tf.range(tf.rank(tensor))[batch_axis:], tf.range(batch_axis)), axis=0)
                    tensor = tf.transpose(tensor, perm=perm)

                gathered_tensor = tf.gather(params=tensor, indices=beam_indices, axis=1, batch_dims=1)
                if batch_axis > 0:
                    
                    perm = tf.concat((tf.range(tf.rank(tensor))[batch_axis:], tf.range(batch_axis)), axis=0)
                    perm = tf.math.invert_permutation(perm)
                    gathered_tensor = tf.transpose(gathered_tensor, perm=perm)

                return gathered_tensor

            return tf.nest.map_structure(gather_fn, nested)

        
        logits_processor = logits_processor if logits_processor is not None else TFLogitsProcessorList()

        max_length = max_length if max_length is not None else self.config.max_length
        pad_token_id = pad_token_id if pad_token_id is not None else self.config.pad_token_id
        eos_token_id = eos_token_id if eos_token_id is not None else self.config.eos_token_id
        num_return_sequences = (
            num_return_sequences if num_return_sequences is not None else self.config.num_return_sequences
        )

        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        output_scores = output_scores if output_scores is not None else self.config.output_scores
        return_dict_in_generate = (
            return_dict_in_generate if return_dict_in_generate is not None else self.config.return_dict_in_generate
        )

        length_penalty = length_penalty if length_penalty is not None else self.config.length_penalty
        early_stopping = early_stopping if early_stopping is not None else self.config.early_stopping

        use_xla = not tf.executing_eagerly()
        
        
        model_name = str(self.decoder) if "EncoderDecoder" in str(self) else str(self)
        cache_batch_axis = 1 if any([model_prefix in model_name for model_prefix in ("TFGPT2", "TFCTRL")]) else 0
        
        needs_full_input = "use_mems" in set(inspect.signature(self.prepare_inputs_for_generation).parameters.keys())

        
        scores = [] if (return_dict_in_generate and output_scores) else None
        decoder_attentions = [] if (return_dict_in_generate and output_attentions) else None
        cross_attentions = [] if (return_dict_in_generate and output_attentions) else None
        decoder_hidden_states = [] if (return_dict_in_generate and output_hidden_states) else None

        "xla-compileable" generate function
        batch_size, num_beams, cur_len = shape_list(input_ids)

        
        input_ids_padding = tf.ones((batch_size, num_beams, max_length - cur_len), dtype=tf.int32) * (
            pad_token_id or 0
        )
        running_sequences = tf.concat([input_ids, input_ids_padding], axis=-1)
        sequences = tf.ones((batch_size, num_beams, max_length), dtype=tf.int32) * (pad_token_id or 0)

        
        is_sent_finished = tf.zeros((batch_size, num_beams), dtype=tf.bool)

        
        running_scores = tf.tile(
            tf.expand_dims(tf.convert_to_tensor([0.0] + [-1.0e9] * (num_beams - 1)), axis=0), [batch_size, 1]
        )
        scores = tf.ones((batch_size, num_beams)) * -1.0e9

        
        if "encoder_outputs" in model_kwargs:
            model_kwargs["encoder_outputs"]["last_hidden_state"] = flatten_beam_dim(
                model_kwargs["encoder_outputs"]["last_hidden_state"]
            )
        if "attention_mask" in model_kwargs:
            model_kwargs["attention_mask"] = flatten_beam_dim(model_kwargs["attention_mask"])

        "xla-compile-able" stop-condition and auto-regressive function
        
        def beam_search_cond_fn(
            cur_len,
            running_sequences,
            running_scores,
            sequences,
            scores,
            is_sent_finished,
            model_kwargs,
        ):
            """
            Beam Search termination condition function -- halts the generation loop if any of these conditions becomes
            False
            """
            
            not_max_length_yet = cur_len < max_length

            
            best_running_score = running_scores[:, :1] / (max_length**length_penalty)
            worst_finished_score = tf.where(
                is_sent_finished, tf.math.reduce_min(scores, axis=1, keepdims=True), -1.0e9
            )
            improvement_still_possible = tf.math.reduce_all(worst_finished_score < best_running_score)

            
            still_open_beam = ~(tf.math.reduce_all(is_sent_finished) & early_stopping)

            return not_max_length_yet & (still_open_beam | improvement_still_possible)

        def beam_search_body_fn(
            cur_len,
            running_sequences,
            running_scores,
            sequences,
            scores,
            is_sent_finished,
            model_kwargs,
        ):
            """
            Beam Search iterative update function -- each iteration adds a new token and updates the best sequences
            seen so far
            """
            
            if model_kwargs.get("past") is None or needs_full_input:
                input_ids = running_sequences[:, :, :cur_len]
            else:
                input_ids = tf.expand_dims(running_sequences[:, :, cur_len - 1], -1)
            model_inputs = self.prepare_inputs_for_generation(flatten_beam_dim(input_ids), **model_kwargs)
            model_outputs = self(
                **model_inputs,
                return_dict=True,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
            )
            logits = unflatten_beam_dim(model_outputs.logits[:, -1], batch_size, num_beams)

            
            if not use_xla and return_dict_in_generate:
                if output_scores:
                    scores.append(model_outputs.logits[:, -1])
                if output_attentions and self.config.is_encoder_decoder:
                    decoder_attentions.append(model_outputs.decoder_attentions)
                elif output_attentions and not self.config.is_encoder_decoder:
                    decoder_attentions.append(model_outputs.attentions)
                    if self.config.is_encoder_decoder:
                        cross_attentions.append(model_outputs.cross_attentions)

                if output_hidden_states and self.config.is_encoder_decoder:
                    decoder_hidden_states.append(model_outputs.decoder_hidden_states)
                elif output_hidden_states and self.config.is_encoder_decoder:
                    decoder_hidden_states.append(model_outputs.hidden_states)

            
            
            
            log_probs = tf.nn.log_softmax(logits)
            log_probs = logits_processor(flatten_beam_dim(running_sequences), flatten_beam_dim(log_probs), cur_len)
            log_probs = unflatten_beam_dim(log_probs, batch_size, num_beams)
            log_probs = log_probs + tf.expand_dims(running_scores, axis=2)
            vocab_size = log_probs.shape[2]
            log_probs = tf.reshape(log_probs, (batch_size, num_beams * vocab_size))

            
            
            
            
            
            
            
            
            
            
            beams_to_keep = 2 * num_beams
            topk_log_probs, topk_indices = tf.math.top_k(log_probs, k=beams_to_keep)
            topk_beam_indices = topk_indices // vocab_size
            topk_running_sequences = gather_beams(running_sequences, topk_beam_indices)
            topk_ids = topk_indices % vocab_size

            
            indices_batch = tf.repeat(tf.range(batch_size), [beams_to_keep])
            indices_beam = tf.tile(tf.range(beams_to_keep), [batch_size])
            update_indices = tf.stack(
                [indices_batch, indices_beam, tf.broadcast_to(cur_len, [batch_size * beams_to_keep])], axis=-1
            )
            topk_sequences = tf.tensor_scatter_nd_update(
                tensor=topk_running_sequences,
                indices=update_indices,
                updates=tf.reshape(topk_ids, [batch_size * beams_to_keep]),
            )

            
            
            
            
            eos_in_next_token = topk_sequences[:, :, cur_len] == eos_token_id
            if eos_token_id is None:
                eos_in_next_token = tf.broadcast_to(eos_in_next_token, topk_sequences[:, :, cur_len].shape)
            did_topk_just_finished = eos_in_next_token & tf.broadcast_to(
                tf.concat((tf.ones((num_beams), dtype=tf.bool), tf.zeros((num_beams), dtype=tf.bool)), axis=0),
                shape_list(eos_in_next_token),
            )

            
            
            running_topk_log_probs = topk_log_probs + tf.cast(eos_in_next_token, tf.float32) * -1.0e9

            
            
            
            next_topk_indices = tf.math.top_k(running_topk_log_probs, k=num_beams)[1]
            next_running_sequences, next_running_scores = gather_beams(
                [topk_sequences, running_topk_log_probs], next_topk_indices
            )

            
            
            
            
            
            topk_log_probs = topk_log_probs / (tf.cast(cur_len, dtype=tf.float32) ** length_penalty)
            beams_in_batch_are_full = (
                tf.broadcast_to(
                    tf.math.reduce_all(is_sent_finished, axis=-1, keepdims=True), shape_list(did_topk_just_finished)
                )
                & early_stopping
            )
            add_penalty = ~did_topk_just_finished | beams_in_batch_are_full
            topk_log_probs += tf.cast(add_penalty, tf.float32) * -1.0e9

            
            
            
            merged_sequences = tf.concat([sequences, topk_sequences], axis=1)
            merged_scores = tf.concat([scores, topk_log_probs], axis=1)
            merged_is_sent_finished = tf.concat([is_sent_finished, did_topk_just_finished], axis=1)
            topk_merged_indices = tf.math.top_k(merged_scores, k=num_beams)[1]
            next_sequences, next_scores, next_is_sent_finished = gather_beams(
                [merged_sequences, merged_scores, merged_is_sent_finished], topk_merged_indices
            )

            
            
            
            cur_len = cur_len + 1
            if "past_key_values" in model_outputs:
                cache = tf.nest.map_structure(
                    lambda tensor: unflatten_beam_dim(tensor, batch_size, num_beams, batch_axis=cache_batch_axis),
                    model_outputs.past_key_values,
                )
                next_running_indices = gather_beams(topk_beam_indices, next_topk_indices)
                next_cache = gather_beams(cache, next_running_indices, batch_axis=cache_batch_axis)
                model_outputs["past_key_values"] = tf.nest.map_structure(
                    lambda tensor: flatten_beam_dim(tensor, batch_axis=cache_batch_axis), next_cache
                )

            if use_xla:
                next_model_kwargs = self._update_model_kwargs_for_xla_generation(
                    model_outputs=model_outputs,
                    model_kwargs=model_kwargs,
                    cur_len=cur_len,
                    max_length=max_length,
                    batch_size=(batch_size * num_beams),
                    is_encoder_decoder=self.config.is_encoder_decoder,
                    batch_axis=cache_batch_axis,
                )
            else:
                next_model_kwargs = self._update_model_kwargs_for_generation(
                    model_outputs, model_kwargs, is_encoder_decoder=self.config.is_encoder_decoder
                )

                
                if model_kwargs.get("past", None) is None:
                    
                    model_kwargs.pop("past", None)

            return (
                cur_len,
                next_running_sequences,
                next_running_scores,
                next_sequences,
                next_scores,
                next_is_sent_finished,
                next_model_kwargs,
            )

        
        
        (
            cur_len,
            running_sequences,
            running_scores,
            sequences,
            scores,
            is_sent_finished,
            model_kwargs,
        ) = beam_search_body_fn(
            cur_len, running_sequences, running_scores, sequences, scores, is_sent_finished, model_kwargs
        )

        
        
        if beam_search_cond_fn(
            cur_len, running_sequences, running_scores, sequences, scores, is_sent_finished, model_kwargs
        ):
            maximum_iterations = max_length - cur_len
            cur_len, running_sequences, running_scores, sequences, scores, is_sent_finished, _ = tf.while_loop(
                beam_search_cond_fn,
                beam_search_body_fn,
                (cur_len, running_sequences, running_scores, sequences, scores, is_sent_finished, model_kwargs),
                maximum_iterations=maximum_iterations,
            )

        
        
        
        none_finished = tf.math.reduce_any(is_sent_finished, axis=1)
        sequences = tf.where(none_finished[:, None, None], sequences, running_sequences)
        scores = tf.where(none_finished[:, None], scores, running_scores)

        
        sequences = flatten_beam_dim(sequences[:, :num_return_sequences, :])
        scores = flatten_beam_dim(scores[:, :num_return_sequences])

        if not use_xla:
            
            sequences = sequences[:, :cur_len]

        if return_dict_in_generate:
            if self.config.is_encoder_decoder:
                
                encoder_attentions = model_kwargs["encoder_outputs"].get("attentions") if output_attentions else None
                encoder_hidden_states = (
                    model_kwargs["encoder_outputs"].get("hidden_states") if output_hidden_states else None
                )

                return TFBeamSearchEncoderDecoderOutput(
                    sequences=sequences,
                    scores=scores,
                    encoder_attentions=encoder_attentions,
                    encoder_hidden_states=encoder_hidden_states,
                    decoder_attentions=decoder_attentions,
                    cross_attentions=cross_attentions,
                    decoder_hidden_states=decoder_hidden_states,
                )
            else:
                return TFBeamSearchDecoderOnlyOutput(
                    sequences=sequences,
                    scores=scores,
                    attentions=decoder_attentions,
                    hidden_states=decoder_hidden_states,
                )
        else:
            return sequences


def _create_next_token_logits_penalties(input_ids, logits, repetition_penalty):
    
    token_penalties = np.ones(shape_list(logits))
    prev_input_ids = [np.unique(input_id) for input_id in input_ids.numpy()]
    for i, prev_input_id in enumerate(prev_input_ids):
        logit_penalized = logits[i].numpy()[prev_input_id]
        logit_penalties = np.zeros(logit_penalized.shape)
        
        logit_penalties[logit_penalized < 0] = repetition_penalty
        logit_penalties[logit_penalized > 0] = 1 / repetition_penalty
        np.put(token_penalties[i], prev_input_id, logit_penalties)
    return tf.convert_to_tensor(token_penalties, dtype=tf.float32)


def calc_banned_ngram_tokens(prev_input_ids, num_hypos, no_repeat_ngram_size, cur_len):
    
    if cur_len + 1 < no_repeat_ngram_size:
        
        return [[] for _ in range(num_hypos)]
    generated_ngrams = [{} for _ in range(num_hypos)]
    for idx in range(num_hypos):
        gen_tokens = prev_input_ids[idx].numpy().tolist()
        generated_ngram = generated_ngrams[idx]
        for ngram in zip(*[gen_tokens[i:] for i in range(no_repeat_ngram_size)]):
            prev_ngram_tuple = tuple(ngram[:-1])
            generated_ngram[prev_ngram_tuple] = generated_ngram.get(prev_ngram_tuple, []) + [ngram[-1]]

    def _get_generated_ngrams(hypo_idx):
        
        start_idx = cur_len + 1 - no_repeat_ngram_size
        ngram_idx = tuple(prev_input_ids[hypo_idx, start_idx:cur_len].numpy().tolist())
        return generated_ngrams[hypo_idx].get(ngram_idx, [])

    banned_tokens = [_get_generated_ngrams(hypo_idx) for hypo_idx in range(num_hypos)]
    return banned_tokens


def calc_banned_bad_words_ids(prev_input_ids, bad_words_ids):
    banned_tokens = []

    def _tokens_match(prev_tokens, tokens):
        if len(tokens) == 0:
            
            return True
        if len(tokens) > len(prev_tokens):
            
            return False

        if prev_tokens[-len(tokens) :] == tokens:
            
            return True
        else:
            return False

    for prev_input_ids_slice in prev_input_ids:
        banned_tokens_slice = []

        for banned_token_seq in bad_words_ids:
            assert (
                len(banned_token_seq) > 0
            ), f"Banned words token sequences { bad_words_ids} cannot have an empty list"

            if _tokens_match(prev_input_ids_slice.numpy().tolist(), banned_token_seq[:-1]) is False:
                
                continue

            banned_tokens_slice.append(banned_token_seq[-1])

        banned_tokens.append(banned_tokens_slice)

    return banned_tokens


def tf_top_k_top_p_filtering(logits, top_k=0, top_p=1.0, filter_value=-float("Inf"), min_tokens_to_keep=1):
    """
    Filter a distribution of logits using top-k and/or nucleus (top-p) filtering

    Args:
        logits: logits distribution shape (batch size, vocabulary size)
        top_k (`int`, *optional*, defaults to 0):
            If > 0, only keep the top k tokens with highest probability (top-k filtering)
        top_p (`float`, *optional*, defaults to 1.0):
            If < 1.0, only keep the top tokens with cumulative probability >= top_p (nucleus filtering). Nucleus
            filtering is described in Holtzman et al. (http://arxiv.org/abs/1904.09751)
        min_tokens_to_keep (`int`, *optional*, defaults to 1):
            Minimumber of tokens we keep per batch example in the output.

    From: https://gist.github.com/thomwolf/1a5a29f6962089e871b94cbd09daf317
    """
    logits_shape = shape_list(logits)

    if top_k > 0:
        top_k = min(max(top_k, min_tokens_to_keep), logits_shape[-1])  
        
        indices_to_remove = logits < tf.math.top_k(logits, k=top_k)[0][..., -1, None]
        logits = tf.where(indices_to_remove, filter_value, logits)
    if top_p < 1.0:
        sorted_indices = tf.argsort(logits, direction="DESCENDING")
        sorted_logits = tf.gather(
            logits, sorted_indices, axis=-1, batch_dims=1
        )  

        cumulative_probs = tf.math.cumsum(stable_softmax(sorted_logits, axis=-1), axis=-1)

        
        sorted_indices_to_remove = cumulative_probs > top_p

        if min_tokens_to_keep > 1:
            
            sorted_indices_to_remove = tf.concat(
                [
                    tf.zeros_like(sorted_indices_to_remove[:, :min_tokens_to_keep]),
                    sorted_indices_to_remove[:, min_tokens_to_keep:],
                ],
                -1,
            )

        
        sorted_indices_to_remove = tf.concat(
            [tf.zeros_like(sorted_indices_to_remove[:, :1]), sorted_indices_to_remove[:, :-1]],
            -1,
        )
        
        indices_to_remove = scatter_values_on_batch_indices(sorted_indices_to_remove, sorted_indices)
        logits = tf.where(indices_to_remove, filter_value, logits)
    return logits


def scatter_values_on_batch_indices(values, batch_indices):
    shape = shape_list(batch_indices)
    
    broad_casted_batch_dims = tf.reshape(tf.broadcast_to(tf.expand_dims(tf.range(shape[0]), axis=-1), shape), [1, -1])
    
    pair_indices = tf.transpose(tf.concat([broad_casted_batch_dims, tf.reshape(batch_indices, [1, -1])], 0))
    
    return tf.scatter_nd(pair_indices, tf.reshape(values, [-1]), shape)


def sample_without_replacement(logits, num_samples):
    """
    categorical sampling without replacement is currently not implemented the gumbel-max trick will do for now see
    https://github.com/tensorflow/tensorflow/issues/9260 for more info
    """
    z = -tf.math.log(tf.random.uniform(shape_list(logits), 0, 1))
    _, indices = tf.nn.top_k(logits + z, num_samples)
    return indices


class BeamHypotheses(object):
    def __init__(self, num_beams, max_length, length_penalty, early_stopping):
        """
        Initialize n-best list of hypotheses.
        """
        self.max_length = max_length - 1  
        self.length_penalty = length_penalty
        self.early_stopping = early_stopping
        self.num_beams = num_beams
        self.beams = []
        self.worst_score = 1e9

    def __len__(self):
        """
        Number of hypotheses in the list.
        """
        return len(self.beams)

    def add(self, hyp, sum_logprobs):
        """
        Add a new hypothesis to the list.
        """
        score = sum_logprobs / len(hyp) ** self.length_penalty
        if len(self) < self.num_beams or score > self.worst_score:
            self.beams.append((score, hyp))
            if len(self) > self.num_beams:
                sorted_scores = sorted([(s, idx) for idx, (s, _) in enumerate(self.beams)])
                del self.beams[sorted_scores[0][1]]
                self.worst_score = sorted_scores[1][0]
            else:
                self.worst_score = min(score, self.worst_score)

    def is_done(self, best_sum_logprobs, cur_len):
        """
        If there are enough hypotheses and that none of the hypotheses being generated can become better than the worst
        one in the heap, then we are done with this sentence.
        """
        if len(self) < self.num_beams:
            return False
        elif self.early_stopping:
            return True
        else:
            cur_score = best_sum_logprobs / cur_len**self.length_penalty
            ret = self.worst_score >= cur_score
            return ret
