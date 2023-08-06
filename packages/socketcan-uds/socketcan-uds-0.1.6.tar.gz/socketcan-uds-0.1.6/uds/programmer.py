""" module:: uds.programmer
    :platform: Posix
    :synopsis: A class file for a uds programmer
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
from abc import ABC, abstractmethod

from enum import IntEnum

from uds.common import *

from uds.client import UdsClient

import logging


class ProgrammerStates(IntEnum):
    # General States
    ProgrammingFileNotLoaded = 0
    NotConnected = 1
    Connected = 2

    PreProgramming = 3

    DeviceUnlocked = 4

    BlockProgramming = 5

    PostProgramming = 6

    ProgrammingFinished = 7


class UdsProgrammerABC(ABC):
    """
    Abstract Base Class for an UDS Programmer class
    """

    def __init__(self,
                 client: Optional[UdsClient] = None,
                 ):
        """
        Constructor

        :param client: A UdsClient for the uds services layer. Optional
                       Theoretically this can be created after reading a programming file.
        """
        self._logger = logging.getLogger(__name__)
        self._client = client

        self._programming_file = None
        self._current_state = None
        self._progress = None

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, val):
        self._progress = val

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, val):
        self._current_state = val

    @abstractmethod
    def load_programming_file(self, filepath: str) -> None:
        """
        1st phase of programming. Loading a programming file.
        Although uds has been standardized, the programming sequences have not and basically every EOM has
        their own flavor. Since ODX based formats have emerged, namely PDX, a programming ODX format,
        a programming file provides
           - binary data: the actual binaries to be programmed
           - means of communication with the target device: typically CAN IDs for an ISOTP channel
           - device compatibility checks based on what identification the device provides,
             e.g. a part number is provided by read data by id
           - device unlock and signature methods, e.g. used crypto functions and keys
           - meta data for each binary data:
             - where the binary goes, e.g. address or index of a binary block and
               subsequently if the location has to be erased in case of flash memory
             - precalculated hashes and signatures for binary blocks
             - binary data may be encrypted or compressed and the programming
               application must know this to populate the corresponding uds services
        This abstracted programmer must obtain all necessary information from the programming file.
        A OrderedDict of blocks has to be provided, ordered because because it matters in which sequence
        blocks are programmed. An item must provide meta data on the block, the definition is
        block_id: {"block_name": str,  # something to display
                   "block_address": int,  # where to put this block
                   "erase_before_download": bool,  # erase flag for destinations that need to be erased, e.g. flash
                   "uds_data_format_identifier": int, # a parameter for request download, e.g. compressed, encrypted
                   "binary_data": bytes,  # the actual data of the block, can be compressed or encrypted
                  }
        There can be general information on communication parameters as well.
        For example, some devices can't handle address items or size items other then 4bytes. In that case the item
        "uds_address_and_length_format_identifier": int, # parameter of request download
        has to be filled. To be continued...
        """

    @abstractmethod
    def pre_programming(self) -> bool:
        """
        2nd phase of programming
        Pre_programming:
        It consists of a couple of steps that occur linear.
        - Identification Check (Application / Optional)
          In case the programming file provides information or identification patterns on the target device,
          this should be checked against the connected device.
        - Preconditions Check (Application)
          An ECU must perform some task, so it must be asked if it is safe to purge regular operation,
          reboot and stay in bootloader without starting application.
        - Preparations Step (Application)
          Any necessary preparation, e.g. disable the settings of DTCs and stop all unnecessary communication.
          This is not actually plausible because when a programming session is started, the scope of operation
          of the ecu typically is very small, so it would not do anything other than handle diagnostic requests.
          It may even happen that an ECU does tell it's communication partners that it is not available for a limited
          time, i.e. like you tell your neighbors that your on holiday for the weekend, so they don't miss you
          and hopefully water your plants.
        - Transition to Programming Session (Application -> Bootloader)
          The most obvious step last but not least, the start of the programming session, which typically involves
          a reboot to bootloader, and setting some flags before, so bootloader waits for programming instead
          of starting application.
          This phase should also contain a sanity check if the programming session has been reached.

        :return: True if met, False otherwise
        """

    # 3rd phase of programming - the programming in programming session
    # this requires a state machine which is not yet written, however tasks during programming can be
    # abstracted into separate functions.

    @abstractmethod
    def unlock_device(self) -> bool:
        """
        Unlock the device for programming.
        Access to uds services required for programming usually require privileged access that can be gained by
        unlocking the device via security access methods. This procedure should be done in this function.

        :return: True if successful, False otherwise
        """

    @abstractmethod
    def pre_block_download(self) -> bool:
        """
        Prepare a block before download.
        :return: True if successful, False otherwise
        """

    def download_block(self,
                       addr: int,
                       data: bytes,
                       compression_method: CompressionMethod = CompressionMethod.NO_COMPRESSION,
                       encryption_method: EncryptionMethod = EncryptionMethod.NO_ENCRYPTION,
                       transfer_request_parameters: bytes = bytes()) -> True:
        """
        Download a block.
        :param addr: The address of the upload. Hardcoded to 32bit for now.
        :param data: The data to be transferred.
        :param compression_method: The method of compression.
        :param encryption_method: The method of encryption.
        :param transfer_request_parameters: A never used manufacturer specific value.
        :return: Nothing.
        """
        size = len(data)
        self._logger.debug("Download Block - Request Download addr {0} size {1}".format(addr, size))
        resp = self._client.request_download(addr=addr,
                                             size=size,
                                             compression_method=compression_method,
                                             encryption_method=encryption_method)
        block_size = resp.get("max_block_length")

        for chunk_idx, chunk_bytes in enumerate(
                [data[idx:idx + block_size] for idx in range(0, len(data), block_size)]):
            self._logger.debug(
                "Download Block - Transfer Data Block {0} Size {1}".format(chunk_idx + 1, len(chunk_bytes)))
            self._client.transfer_data(block_sequence_counter=chunk_idx + 1,
                                       data=chunk_bytes)
        self._logger.debug("Download Block - Request Transfer Exit")
        self._client.request_transfer_exit(transfer_request_parameters=transfer_request_parameters)
        self._logger.debug("Download Block - Complete")

        success = True
        return success

    @abstractmethod
    def post_block_download(self) -> bool:
        """
        Check a block after download.
        :return: True if successful, False otherwise
        """

    @abstractmethod
    def post_programming(self) -> bool:
        """
        Finish the programming, e.g. reset the device.
        :return: True if successful, False otherwise
        """


class ExampleUdsProgrammer(UdsProgrammerABC):
    def load_programming_file(self, filepath: str) -> bool:
        """
        Load the programming file. Save filepath to private variable
        for an easy example.
        :param filepath: The filepath.
        :return: True if successful.
        """
        self._programming_file = filepath
        return True

    def pre_programming(self) -> bool:
        """
        Check if the logical preconditions for programming are fulfilled.
        You won't flash an engine ecu while the engine is running, would you?
        Well it can be done in some rare cases.
        :return: True if successful.
        """
        check_programming_did = 0xBEEF
        data = self._client.read_data_by_id(did=check_programming_did).get("data")
        status = bool.from_bytes(data, "big")
        return status

    def unlock_device(self) -> bool:
        """
        Execute seed and key routine to unlock the device.
        :return: True if successful.
        """
        security_level = 1
        seed = self._client.security_access(security_level=security_level).get("seed")
        key = struct.pack(">I", struct.unpack(">I", seed)[0] + 1)
        self._client.security_access(security_level=security_level + 1, key=key)
        success = True
        return success

    def pre_block_download(self) -> bool:
        """
        Write the workshop name into the device for
        an easy example.
        :return: True if successful.
        """
        workshop_did = 0xCAFE
        self._client.write_data_by_id(did=workshop_did, data="1234".encode())
        success = True
        return success

    def post_block_download(self) -> bool:
        """
        Execute a check routine in device.
        :return: True if successful.
        """
        self._client.routine_control(routine_control_type=RoutineControlType.StartRoutine,
                                     routine_id=0x1234,
                                     data=bytes.fromhex("11 22 33 44 55 66 77 88"))
        success = True
        return success

    def post_programming(self) -> bool:
        """
        Write the programming date for an easy example.
        :return: True if successful.
        """
        programming_date_did = 0x4242
        self._client.write_data_by_id(did=programming_date_did, data=bytes.fromhex("11 22 33 44"))
        success = True
        return success
