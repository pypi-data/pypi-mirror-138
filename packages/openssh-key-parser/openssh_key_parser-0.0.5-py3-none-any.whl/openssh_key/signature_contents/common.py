import abc
import typing
import warnings
from openssh_key import utils

from openssh_key.key_params import PrivateKeyParamsTypeVar, PublicKeyParamsTypeVar
from openssh_key.pascal_style_byte_stream import PascalStyleByteStream



SignatureContentsTypeVar = typing.TypeVar(
    'SignatureContentsTypeVar',
    bound='SignatureContents[typing.Any, typing.Any, typing.Any]'
)


class SignatureContents(
    typing.Generic[
        PublicKeyParamsTypeVar,
        PrivateKeyParamsTypeVar,
        SignatureContentsTypeVar
    ],
    abc.ABC
):
    # TODO This represents ONLY the section AFTER the identifier
    @abc.abstractmethod
    def verify(
        self,
        public_key_params: PublicKeyParamsTypeVar,
        challenge: bytes,
    ) -> bool:
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def sign(
        cls,
        private_key_params: PrivateKeyParamsTypeVar,
        challenge: bytes,
    ) -> SignatureContentsTypeVar:
        raise NotImplementedError()
