# pylint: disable=line-too-long,too-many-lines,missing-docstring,arguments-differ,unused-argument
import mxnet as mx
from mxnet import init
from mxnet.gluon import nn
from mxnet.gluon.nn import HybridBlock
from ..inception import inception_v3

__all__ = ['inceptionv3_ucf101', 'inceptionv3_hmdb51', 'inceptionv3_kinetics400',
           'inceptionv3_sthsthv2']

class ActionRecInceptionV3(HybridBlock):
    r"""InceptionV3 model for video action recognition
    Christian Szegedy, etal, Rethinking the Inception Architecture for Computer Vision, CVPR 2016
    https://arxiv.org/abs/1512.00567
    Limin Wang, etal, Towards Good Practices for Very Deep Two-Stream ConvNets, arXiv 2015
    https://arxiv.org/abs/1507.02159
    Limin Wang, etal, Temporal Segment Networks: Towards Good Practices for Deep Action Recognition, ECCV 2016
    https://arxiv.org/abs/1608.00859

    Parameters
    ----------
    nclass : int
        Number of classes in the training dataset.
    pretrained_base : bool or str, optional, default is True.
        Load pretrained base network, the extra layers are randomized. Note that
        if pretrained is `True`, this has no effect.
    partial_bn : bool, default False.
        Freeze all batch normalization layers during training except the first layer.
    dropout_ratio : float, default is 0.5.
        The dropout rate of a dropout layer.
        The larger the value, the more strength to prevent overfitting.
    init_std : float, default is 0.001.
        Standard deviation value when initialize the dense layers.
    num_segments : int, default is 1.
        Number of segments used to evenly divide a video.
    num_crop : int, default is 1.
        Number of crops used during evaluation, choices are 1, 3 or 10.

    Input: a single video frame or N images from N segments when num_segments > 1
    Output: a single predicted action label
    """
    def __init__(self, nclass, pretrained_base=True,
                 partial_bn=True, dropout_ratio=0.5, init_std=0.001,
                 num_segments=1, num_crop=1, **kwargs):
        super(ActionRecInceptionV3, self).__init__()
        self.dropout_ratio = dropout_ratio
        self.init_std = init_std
        self.num_segments = num_segments
        self.num_crop = num_crop
        self.feat_dim = 2048

        pretrained_model = inception_v3(pretrained=pretrained_base, partial_bn=partial_bn, **kwargs)
        self.features = pretrained_model.features
        def update_dropout_ratio(block):
            if isinstance(block, nn.basic_layers.Dropout):
                block._rate = self.dropout_ratio
        self.apply(update_dropout_ratio)
        self.output = nn.Dense(units=nclass, in_units=self.feat_dim,
                               weight_initializer=init.Normal(sigma=self.init_std))
        self.output.initialize()

    def hybrid_forward(self, F, x):
        x = self.features(x)

        # segmental consensus
        x = F.reshape(x, shape=(-1, self.num_segments * self.num_crop, self.feat_dim))
        x = F.mean(x, axis=1)

        x = self.output(x)
        return x

def inceptionv3_ucf101(nclass=101, pretrained=False, pretrained_base=True,
                       use_tsn=False, num_segments=1, num_crop=1, partial_bn=True,
                       ctx=mx.cpu(), root='~/.mxnet/models', **kwargs):
    r"""InceptionV3 model trained on UCF101 dataset.

    Parameters
    ----------
    nclass : int.
        Number of categories in the dataset.
    pretrained : bool or str.
        Boolean value controls whether to load the default pretrained weights for model.
        String value represents the hashtag for a certain version of pretrained weights.
    pretrained_base : bool or str, optional, default is True.
        Load pretrained base network, the extra layers are randomized. Note that
        if pretrained is `True`, this has no effect.
    ctx : Context, default CPU.
        The context in which to load the pretrained weights.
    root : str, default $MXNET_HOME/models
        Location for keeping the model parameters.
    num_segments : int, default is 1.
        Number of segments used to evenly divide a video.
    num_crop : int, default is 1.
        Number of crops used during evaluation, choices are 1, 3 or 10.
    partial_bn : bool, default False.
        Freeze all batch normalization layers during training except the first layer.
    """
    model = ActionRecInceptionV3(nclass=nclass,
                                 partial_bn=partial_bn,
                                 pretrained_base=pretrained_base,
                                 num_segments=num_segments,
                                 num_crop=num_crop,
                                 dropout_ratio=0.8,
                                 init_std=0.001)

    if pretrained:
        from ..model_store import get_model_file
        model.load_parameters(get_model_file('inceptionv3_ucf101',
                                             tag=pretrained, root=root))
        from ...data import UCF101Attr
        attrib = UCF101Attr()
        model.classes = attrib.classes
    model.collect_params().reset_ctx(ctx)
    return model

def inceptionv3_hmdb51(nclass=51, pretrained=False, pretrained_base=True,
                       use_tsn=False, num_segments=1, num_crop=1, partial_bn=True,
                       ctx=mx.cpu(), root='~/.mxnet/models', **kwargs):
    r"""InceptionV3 model trained on HMDB51 dataset.

    Parameters
    ----------
    nclass : int.
        Number of categories in the dataset.
    pretrained : bool or str.
        Boolean value controls whether to load the default pretrained weights for model.
        String value represents the hashtag for a certain version of pretrained weights.
    pretrained_base : bool or str, optional, default is True.
        Load pretrained base network, the extra layers are randomized. Note that
        if pretrained is `True`, this has no effect.
    ctx : Context, default CPU.
        The context in which to load the pretrained weights.
    root : str, default $MXNET_HOME/models
        Location for keeping the model parameters.
    num_segments : int, default is 1.
        Number of segments used to evenly divide a video.
    num_crop : int, default is 1.
        Number of crops used during evaluation, choices are 1, 3 or 10.
    partial_bn : bool, default False.
        Freeze all batch normalization layers during training except the first layer.
    """
    model = ActionRecInceptionV3(nclass=nclass,
                                 partial_bn=partial_bn,
                                 pretrained_base=pretrained_base,
                                 num_segments=num_segments,
                                 num_crop=num_crop,
                                 dropout_ratio=0.8,
                                 init_std=0.001)

    if pretrained:
        from ..model_store import get_model_file
        model.load_parameters(get_model_file('inceptionv3_hmdb51',
                                             tag=pretrained, root=root))
        from ...data import HMDB51Attr
        attrib = HMDB51Attr()
        model.classes = attrib.classes
    model.collect_params().reset_ctx(ctx)
    return model

def inceptionv3_kinetics400(nclass=400, pretrained=False, pretrained_base=True,
                            tsn=False, num_segments=1, num_crop=1, partial_bn=True,
                            ctx=mx.cpu(), root='~/.mxnet/models', **kwargs):
    r"""InceptionV3 model trained on Kinetics400 dataset.

    Parameters
    ----------
    nclass : int.
        Number of categories in the dataset.
    pretrained : bool or str.
        Boolean value controls whether to load the default pretrained weights for model.
        String value represents the hashtag for a certain version of pretrained weights.
    pretrained_base : bool or str, optional, default is True.
        Load pretrained base network, the extra layers are randomized. Note that
        if pretrained is `True`, this has no effect.
    ctx : Context, default CPU.
        The context in which to load the pretrained weights.
    root : str, default $MXNET_HOME/models
        Location for keeping the model parameters.
    num_segments : int, default is 1.
        Number of segments used to evenly divide a video.
    num_crop : int, default is 1.
        Number of crops used during evaluation, choices are 1, 3 or 10.
    partial_bn : bool, default False.
        Freeze all batch normalization layers during training except the first layer.
    """
    model = ActionRecInceptionV3(nclass=nclass,
                                 partial_bn=partial_bn,
                                 pretrained_base=pretrained_base,
                                 num_segments=num_segments,
                                 num_crop=num_crop,
                                 dropout_ratio=0.5,
                                 init_std=0.01)

    if pretrained:
        from ..model_store import get_model_file
        model.load_parameters(get_model_file('inceptionv3_kinetics400',
                                             tag=pretrained, root=root))
        from ...data import Kinetics400Attr
        attrib = Kinetics400Attr()
        model.classes = attrib.classes
    model.collect_params().reset_ctx(ctx)
    return model

def inceptionv3_sthsthv2(nclass=174, pretrained=False, pretrained_base=True,
                         tsn=False, num_segments=1, num_crop=1, partial_bn=True,
                         ctx=mx.cpu(), root='~/.mxnet/models', **kwargs):
    r"""InceptionV3 model trained on Something-Something-V2 dataset.

    Parameters
    ----------
    nclass : int.
        Number of categories in the dataset.
    pretrained : bool or str.
        Boolean value controls whether to load the default pretrained weights for model.
        String value represents the hashtag for a certain version of pretrained weights.
    pretrained_base : bool or str, optional, default is True.
        Load pretrained base network, the extra layers are randomized. Note that
        if pretrained is `True`, this has no effect.
    ctx : Context, default CPU.
        The context in which to load the pretrained weights.
    root : str, default $MXNET_HOME/models
        Location for keeping the model parameters.
    num_segments : int, default is 1.
        Number of segments used to evenly divide a video.
    num_crop : int, default is 1.
        Number of crops used during evaluation, choices are 1, 3 or 10.
    partial_bn : bool, default False.
        Freeze all batch normalization layers during training except the first layer.
    """
    model = ActionRecInceptionV3(nclass=nclass,
                                 partial_bn=partial_bn,
                                 pretrained_base=pretrained_base,
                                 num_segments=num_segments,
                                 num_crop=num_crop,
                                 dropout_ratio=0.5,
                                 init_std=0.01)

    if pretrained:
        from ..model_store import get_model_file
        model.load_parameters(get_model_file('inceptionv3_sthsthv2',
                                             tag=pretrained, root=root))
        from ...data import SomethingSomethingV2Attr
        attrib = SomethingSomethingV2Attr()
        model.classes = attrib.classes
    model.collect_params().reset_ctx(ctx)
    return model
