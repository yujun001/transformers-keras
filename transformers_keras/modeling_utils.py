import logging
import os

import numpy as np
import tensorflow as tf


def gelu(x):
    """ Gaussian Error Linear Unit.
    Original Implementation of the gelu activation function in Google Bert repo when initially created.
        For information: OpenAI GPT's gelu is slightly different (and gives slightly different results):
        0.5 * x * (1 + torch.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * torch.pow(x, 3))))
        Also see https://arxiv.org/abs/1606.08415
    """
    cdf = 0.5 * (1.0 + tf.math.erf(x / tf.math.sqrt(2.0)))
    return x * cdf


def gelu_new(x):
    """Gaussian Error Linear Unit.
    This is a smoother version of the RELU.
    Original paper: https://arxiv.org/abs/1606.08415
    Args:
        x: float Tensor to perform activation.
    Returns:
        `x` with the GELU activation applied.
    """
    cdf = 0.5 * (1.0 + tf.tanh((np.sqrt(2 / np.pi) * (x + 0.044715 * tf.pow(x, 3)))))
    return x * cdf


def swish(x):
    return x * tf.sigmoid(x)


ACT2FN = {
    "gelu": tf.keras.layers.Activation(gelu),
    "relu": tf.keras.activations.relu,
    "swish": tf.keras.layers.Activation(swish),
    "gelu_new": tf.keras.layers.Activation(gelu_new),
}


def choose_activation(act):
    if isinstance(act, tf.keras.layers.Activation):
        return act
    if isinstance(act, str):
        return ACT2FN[act]
    return act


def initialize(stddev=0.02):
    return tf.keras.initializers.TruncatedNormal(stddev=stddev)


def parse_pretrained_model_files(pretrain_model_dir):
    config_file, ckpt, vocab = None, None, None
    pretrain_model_dir = os.path.abspath(pretrain_model_dir)
    if not os.path.exists(pretrain_model_dir):
        logging.info('pretrain model dir: {} is not exists.'.format(pretrain_model_dir))
        return config_file, ckpt, vocab
    for f in os.listdir(pretrain_model_dir):
        if str(f).endswith('config.json'):
            config_file = os.path.join(pretrain_model_dir, f)
        if 'vocab' in str(f):
            vocab = os.path.join(pretrain_model_dir, f)
        if 'ckpt' in str(f):
            n = '.'.join(str(f).split('.')[:-1])
            ckpt = os.path.join(pretrain_model_dir, n)
    return config_file, ckpt, vocab
