#! /usr/bin/env python3
#
# Copyright (C) 2018  Fx Bricks Inc.
# This file is part of the pfxbrick python module.
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# PFx Brick python API

import hid
from bleak import BleakClient, BleakScanner

from pfxbrick import *
from pfxbrick.pfxfiles import fs_format
from pfxbrick.pfxhelpers import *
from pfxbrick.pfxmsg import *


def find_bricks(show_list=False):
    """
    Enumerate and optionally print a list PFx Bricks currently connected to the USB bus.

    :param boolean show_list: optionally print a list of enumerated PFx Bricks
    :returns: [:obj:`str`] a list of PFx Brick serial numbers
    """
    numBricks = 0
    serials = []
    for dev in hid.enumerate():
        if (
            dev["vendor_id"] == PFX_USB_VENDOR_ID
            and dev["product_id"] == PFX_USB_PRODUCT_ID
        ):
            if dev["serial_number"] not in serials:
                numBricks += 1
                serials.append(dev["serial_number"])
                h = hid.device()
                h.open(PFX_USB_VENDOR_ID, PFX_USB_PRODUCT_ID, dev["serial_number"])
                usb_prod_str = h.get_product_string()
                usb_serno_str = h.get_serial_number_string()
                if show_list == True:
                    print(
                        "%d. %s, Serial No: %s"
                        % (numBricks, usb_prod_str, usb_serno_str)
                    )
                h.close()
    return serials


class PFxBrick:
    """
    Top level PFx Brick object class.

    This class is used to initialize and maintain a communication session
    with a USB connected PFx Brick. Many convenient methods are provided
    to perform tasks such as changing configuration, accessing the file
    system, initiating actions, and more.

    Attributes:
        product_id (:obj:`str`): product ID code reported by the PFx Brick (e.g. 'A204')

        serial_no (:obj:`str`): serial number reported by the PFx Brick, usually 8 digit hexadecimal

        product_desc (:obj:`str`): product descriptor reported by the PFx Brick

        firmware_ver (:obj:`str`): firmware version number reported, 4-digit hex BCD, e.g. '0134' represents v.1.34

        firmware_build (:obj:`str`): firmware build number reported, 4-digit hex BCD

        icd_rev (:obj:`str`): ICD revision number reported, 4-digit hex BCD, e.g. '0336' represents v.3.36
        status (:obj:`int`): status code reported, distinguishes normal and service/recovery mode

        error (:obj:`int`): error code reported

        usb_vid (:obj:`int`): fixed to PFX_USB_VENDOR_ID representing the official USB VID assigned to the PFx Brick

        usb_pid (:obj:`int`): fixed to PFX_USB_PRODUCT_ID representing the official USB PID assigned to the PFx Brick

        usb_manu_str (:obj:`str`): the manufacturer string reported to the host USB interface

        usb_prod_str (:obj:`str`): the product descriptor string reported to the host USB interface

        usb_serno_str (:obj:`str`): the product serial number string reported to the host USB interface

        dev (:obj:`device`): a device handle to the HIDAPI cdef class device

        is_open (:obj:`boolean`): a flag indicating connected session status

        name (:obj:`str`): user defined name of the PFx Brick

        config (:obj:`PFxConfig`): child class to store configuration and settings

        filedir (:obj:`PFxDir`): child class to store the file system directory
    """

    def __init__(self, serial_no=None):
        self.product_id = ""
        self.serial_no = ""
        self.product_desc = ""
        self.firmware_ver = ""
        self.firmware_build = ""
        self.icd_rev = ""
        self.status = 0
        self.error = 0
        self.usb_vid = PFX_USB_VENDOR_ID
        self.usb_pid = PFX_USB_PRODUCT_ID
        self.usb_manu_str = ""
        self.usb_prod_str = ""
        self.usb_serno_str = ""
        self.dev = None
        self.is_open = False
        self.has_bluetooth = False
        self.name = ""

        self.config = PFxConfig()
        self.filedir = PFxDir()
        self.state = PFxState()

        if serial_no is not None:
            self.open(ser_no=serial_no)

    def open(self, ser_no=None):
        """
        Opens a USB communication session with a PFx Brick. If multiple PFx Bricks are
        connected, then a serial number must be specified to connect to a unique PFx Brick.

        :param ser_no: optional serial number to specify a particular PFx Brick if multiple connected
        :returns: boolean indicating open session result
        """
        if ser_no is not None:
            ser_no = ser_no.upper()
        if not self.is_open:
            numBricks = 0
            serials = []
            for dev in hid.enumerate():
                if (
                    dev["vendor_id"] == PFX_USB_VENDOR_ID
                    and dev["product_id"] == PFX_USB_PRODUCT_ID
                ):
                    if dev["serial_number"] not in serials:
                        numBricks += 1
                        serials.append(dev["serial_number"])
            if ser_no is not None and ser_no not in serials:
                print("The PFx Brick with serial number %s was not found." % (ser_no))
            else:
                if numBricks == 0:
                    print("No PFx Bricks are currently connected.")
                elif numBricks > 1 and ser_no is None:
                    print(
                        "There are multiple PFx Bricks connected. Therefore a serial number is required to specify which PFx Brick to connect to."
                    )
                else:
                    self.dev = hid.device()
                    self.dev.open(PFX_USB_VENDOR_ID, PFX_USB_PRODUCT_ID, ser_no)
                    self.usb_manu_str = self.dev.get_manufacturer_string()
                    self.usb_prod_str = self.dev.get_product_string()
                    self.usb_serno_str = self.dev.get_serial_number_string()
                    self.is_open = True
                    self.get_icd_rev()
                    self.config.icd_rev = self.icd_rev
                    self.get_status()
                    if self.product_id in ["A204", "A208", "A216"]:
                        self.has_bluetooth = True
        return self.is_open

    def close(self):
        """
        Closes a USB communication session with a PFx Brick.
        """
        if self.is_open:
            self.dev.close()

    def get_icd_rev(self, silent=False):
        """
        Requests the version of Interface Control Document (ICD)
        the connected PFx Brick supports using the `PFX_CMD_GET_ICD_REV`
        ICD message.  The resulting version number is stored in
        this class and also returned.

        :param boolean silent: flag to optionally silence the status LED blink

        :returns: :obj:`str` ICD version, e.g. "3.38"
        """
        res = cmd_get_icd_rev(self.dev, silent)
        self.icd_rev = uint16_tover(res[1], res[2])
        return self.icd_rev

    def get_status(self):
        """
        Requests the top level operational status of the PFx Brick

        Summary operating status is obtained from the PFx Brick using
        the `PFX_CMD_GET_STATUS ICD` message.  The resulting
        status data is stored in this class and can be queried
        with class member access methods such as `status_str`.

        :returns: None
        """
        res = cmd_get_status(self.dev)
        if res:
            self.status = res[1]
            self.error = res[2]
            self.product_id = uint16_tostr(res[7], res[8])
            self.serial_no = uint32_tostr(res[9], res[10], res[11], res[12])
            self.product_desc = bytes(res[13:37]).decode("utf-8")
            self.firmware_ver = uint16_tover(res[37], res[38])
            self.firmware_build = uint16_tostr(res[39], res[40])

    def status_str(self):
        """
        Returns a summary status string of the PFx Brick

        A human readable string of PFx Brick basic identification and
        and operating status.  A call to the `get_status` method is recommended
        to ensure that the status information is recent.

        :returns: :obj:`str` status string
        """
        s = []
        s.append("USB vendor ID         : 0x%04X" % (self.usb_vid))
        s.append("USB product ID        : 0x%04X" % (self.usb_pid))
        s.append("USB product desc      : %s" % (self.usb_prod_str))
        s.append("USB manufacturer      : %s" % (self.usb_manu_str))
        s.append(
            "PFx Brick product ID  : %s, %s" % (self.product_id, self.product_desc)
        )
        s.append("Serial number         : %s" % (self.serial_no))
        s.append(
            "Firmware version      : %s build %s"
            % (self.firmware_ver, self.firmware_build)
        )
        s.append(
            "Status                : 0x%02X %s"
            % (self.status, get_status_str(self.status))
        )
        s.append(
            "Errors                : 0x%02X %s"
            % (self.error, get_error_str(self.error))
        )
        return "\n".join(s)

    def print_status(self):
        """
        Prints the top level operational status information retrieved
        by a previous call to the get_status method.
        """
        print(self.status_str())

    def get_config(self):
        """
        Retrieves configuration settings from the PFx Brick using
        the `PFX_CMD_GET_CONFIG` ICD message. The configuration data
        is stored in the :obj:`PFxBrick.config` class member variable.
        """
        res = cmd_get_config(self.dev)
        if res:
            self.config.from_bytes(res)

    def print_config(self):
        """
        Prints a summary representation of the PFx Brick configuration
        settings which were retrieved by a previous call to get_config.
        """
        print(str(self.config))

    def set_config(self):
        """
        Writes the contents of the :obj:`PFxConfig` data structure class to
        the PFx Brick using the `PFX_CMD_SET_CONFIG ICD` message.

        It is recommended that the configuration be read from the
        PFx Brick (using `get_config`) before any changes are made to
        the configuration and written back. This ensures that any
        configuration settings which are not desired to be changed
        are left in the same state.
        """
        res = cmd_set_config(self.dev, self.config.to_bytes())

    def reset_factory_config(self):
        """
        Resets the PFx Brick configuration settings to factory defaults.
        """
        res = cmd_set_factory_defaults(self.dev)

    def get_name(self):
        """
        Retrieves the user defined name of the PFx Brick using
        the `PFX_CMD_GET_NAME ICD` message. The name is stored in
        the name class variable as a UTF-8 string.

        :returns: :obj:`str` user defined name
        """
        res = cmd_get_name(self.dev)
        if res:
            self.name = safe_unicode_str(res[1:25])
        return self.name

    def set_name(self, name):
        """
        Sets the user defined name of the PFx Brick using the
        `PFX_CMD_SET_NAME ICD` message.

        :param name: :obj:`str` new name to set (up to 24 character bytes, UTF-8)
        """
        res = cmd_set_name(self.dev, name)

    def get_action_by_address(self, address):
        """
        Retrieves a stored action indexed by address rather than a
        combination of eventID and IR channel.  The address is converted into a
        [eventID, IR channel] pair and the get_action method is
        called with this function as a convenient wrapper.

        :param address: :obj:`int` event/action LUT address (0 - 0x7F)
        :returns: :obj:`PFxAction` class filled with retrieved LUT data
        """
        if address > EVT_LUT_MAX:
            print("Requested action at address %02X is out of range" % (address))
            return None
        else:
            evt, ch = address_to_evtch(address)
            return self.get_action(evt, ch)

    def get_action(self, evtID, ch):
        """
        Retrieves the stored action associated with a particular
        [eventID / IR channel] event. The eventID and channel value
        form a composite address pointer into the event/action LUT
        in the PFx Brick. The address to the LUT is formed as:

        Address[5:2] = event ID
        Address[1:0] = channel

        :param evtID: :obj:`int` event ID LUT address component (0 - 0x20)
        :param channel: :obj:`int` channel index LUT address component (0 - 3)
        :returns: :obj:`PFxAction` class filled with retrieved LUT data
        """
        if ch > 3 or evtID > EVT_ID_MAX:
            print("Requested action (id=%02X, ch=%02X) is out of range" % (evtID, ch))
            return None
        else:
            res = cmd_get_event_action(self.dev, evtID, ch)
            action = PFxAction()
            if res:
                action.from_bytes(res)
            return action

    def set_action_by_address(self, address, action):
        """
        Sets a new stored action in the event/action LUT at the
        address specified. The address is converted into a
        [eventID, IR channel] pair and the set_action method is
        called with this function as a convenient wrapper.

        :param address: :obj:`int` event/action LUT address (0 - 0x7F)
        :param action: :obj:`PFxAction` action data structure class
        """
        if address > EVT_LUT_MAX:
            print("Requested action at address %02X is out of range" % (address))
            return None
        else:
            evt, ch = address_to_evtch(address)
            self.set_action(evt, ch, action)

    def set_action(self, evtID, ch, action):
        """
        Sets a new stored action associated with a particular
        [eventID / IR channel] event. The eventID and channel value
        form a composite address pointer into the event/action LUT
        in the PFx Brick. The address to the LUT is formed as:

        Address[5:2] = event ID
        Address[1:0] = channel

        :param evtID: :obj:`int` event ID LUT address component (0 - 0x20)
        :param ch: :obj:`int` channel index LUT address component (0 - 3)
        :param action: :obj:`PFxAction` action data structure class
        """
        if ch > 3 or evtID > EVT_ID_MAX:
            print("Requested action (id=%02X, ch=%02X) is out of range" % (evtID, ch))
            return None
        else:
            res = cmd_set_event_action(self.dev, evtID, ch, action.to_bytes())

    def test_action(self, action):
        """
        Executes a passed action data structure. This function is
        used to "test" actions to see how they behave. The passed
        action is not stored in the event/action LUT.

        :param action: :obj:`PFxAction` action data structure class
        """
        res = cmd_test_action(self.dev, action.to_bytes())

    def clear_action_by_address(self, address):
        """
        Clears a stored action in the event/action LUT at the
        address specified. The address is converted into a
        [eventID, IR channel] pair and the set_action method is
        called with this function as a convenient wrapper.

        :param address: :obj:`int` event/action LUT address (0 - 0x7F)
                        :obj:`list,tuple,range` specify a list or range of addresses
        """
        if isinstance(address, (list, tuple)):
            addresses = address
        elif isinstance(address, range):
            addresses = [x for x in range]
        else:
            addresses = [address]
        for a in addresses:
            if a > EVT_LUT_MAX:
                print("Requested action at address %02X is out of range" % (a))
                return None
            else:
                evt, ch = address_to_evtch(a)
                self.clear_action(evt, ch)

    def clear_action(self, evtID, ch):
        """
        Clears a stored action associated with a particular
        [eventID / IR channel] event. The eventID and channel value
        form a composite address pointer into the event/action LUT
        in the PFx Brick. The address to the LUT is formed as:

        Address[5:2] = event ID
        Address[1:0] = channel

        :param evtID: :obj:`int` event ID LUT address component (0 - 0x20)
        :param ch: :obj:`int` channel index LUT address component (0 - 3)
        """
        if ch > 3 or evtID > EVT_ID_MAX:
            print("Requested action (id=%02X, ch=%02X) is out of range" % (evtID, ch))
            return None
        else:
            # set to an empty PFxAction to clear
            res = cmd_set_event_action(self.dev, evtID, ch, PFxAction().to_bytes())

    def find_startup_action(self, lightfx=None, soundfx=None, motorfx=None):
        """
        Finds a startup action with one or more specified light, motor, or
        sound fx types.

        :param lightfx: :obj:`int` optional lightfx id
        :param soundfx: :obj:`int` optional soundfx id
        :param motorfx: :obj:`int` optional motorfx id

        :returns: :obj:`PFxAction` action data structure class matching the desired type(s)
        """
        req_matches = 0
        if lightfx is not None:
            req_matches += 1
        if soundfx is not None:
            req_matches += 1
        if motorfx is not None:
            req_matches += 1
        for e in range(EVT_STARTUP_EVENT1, EVT_STARTUP_EVENT8 + 1):
            matches = 0
            action = self.get_action_by_address(e)
            if lightfx is not None and action.lightFxId == lightfx:
                matches += 1
            if soundfx is not None and action.soundFxId == soundfx:
                matches += 1
            if motorfx is not None and action.motorActionId == motorfx:
                matches += 1
            if matches == req_matches:
                return action
        return None

    def set_motor_speed(self, ch, speed, duration=None):
        """
        A convenience wrapper for `PFxAction().set_motor_speed`

        :param ch: [:obj:`int`] a list of motor channels (1-4)
        :param speed: :obj:`int` desired motor speed (-100 to +100)
        :param duration: :obj:`float` optional duration (in seconds) to run motor, runs indefinitely if not specified

        If the duration value is specified, it represents the desired motor
        run time in seconds. Note that this value will be rounded to the
        nearest fixed interval of the DURATION parameter as defined in the ICD
        ranging between 16 fixed values from 0.5 sec to 5 min.
        """
        self.test_action(PFxAction().set_motor_speed(ch, speed, duration=duration))

    def stop_motor(self, ch):
        """
        A convenience wrapper for `PFxAction().stop_motor`

        :param ch: [:obj:`int`] a list of motor channels (1-4)
        """
        self.test_action(PFxAction().stop_motor(ch))

    def light_on(self, ch):
        """
        A convenience wrapper for `PFxAction().light_on`

        :param ch: [:obj:`int`] a list of light channels (1-8)
        """
        self.test_action(PFxAction().light_on(ch))

    def light_off(self, ch):
        """
        A convenience wrapper for `PFxAction().light_off`

        :param ch: [:obj:`int`] a list of light channels (1-8)
        """
        self.test_action(PFxAction().light_off(ch))

    def light_toggle(self, ch):
        """
        A convenience wrapper for `PFxAction().light_toggle`

        :param ch: [:obj:`int`] a list of light channels (1-8)
        """
        self.test_action(PFxAction().light_toggle(ch))

    def set_brightness(self, ch, brightness):
        """
        A convenience wrapper for `PFxAction().set_brightness`

        :param ch: [:obj:`int`] a list of light channels (1-8)
        :param brightness: :obj:`int` brightness (0 - 255 max)
        """
        self.test_action(PFxAction().set_brightness(ch, brightness))

    def combo_light_fx(self, fx, param=[0, 0, 0, 0, 0]):
        """
        A convenience wrapper for `PFxAction().combo_light_fx`

        :param fx: :obj:`int` desired light effect
        :param param: [:obj:`int`] a list of up to 5 light parameters
        """
        self.test_action(PFxAction().combo_light_fx(fx, param=param))

    def light_fx(self, ch, fx, param=[0, 0, 0, 0, 0]):
        """
        A convenience wrapper for `PFxAction().light_fx`

        :param ch: [:obj:`int`] a list of light channels (1-8)
        :param fx: :obj:`int` desired light effect
        :param param: [:obj:`int`] a list of up to 5 light parameters
        """
        self.test_action(PFxAction().light_fx(ch, fx, param=param))

    def sound_fx(self, fx, param=[0, 0], fileID=None):
        """
        A convenience wrapper for `PFxAction().sound_fx`

        :param fx: :obj:`int` desired sound action
        :param param: [:obj:`int`] a list of up to 2 sound parameters
        :param fileID: :obj:`int` file ID of an audio file in the file system
        """
        if fileID is not None:
            fileID = self.file_id_from_str_or_int(fileID)
        self.test_action(PFxAction().sound_fx(fx, param=param, fileID=fileID))

    def play_audio_file(self, fileID):
        """
        A convenience wrapper for `PFxAction().sound_fx`

        :param fileID: :obj:`int` or :obj:`str` file ID or filename of an audio file in the file system
        """
        fileID = self.file_id_from_str_or_int(fileID)
        self.test_action(PFxAction().play_audio_file(fileID=fileID))

    def stop_audio_file(self, fileID):
        """
        A convenience wrapper for `PFxAction().stop_audio_file`

        :param fileID: :obj:`int` or :obj:`str` file ID or filename of an audio file in the file system
        """
        fileID = self.file_id_from_str_or_int(fileID)
        self.test_action(PFxAction().stop_audio_file(fileID=fileID))

    def repeat_audio_file(self, fileID):
        """
        A convenience wrapper for `PFxAction().repeat_audio_file`

        :param fileID: :obj:`int` or :obj:`str` file ID or filename of an audio file in the file system
        """
        fileID = self.file_id_from_str_or_int(fileID)
        self.test_action(PFxAction().repeat_audio_file(fileID=fileID))

    def set_volume(self, volume):
        """
        A convenience wrapper for `PFxAction().set_volume`

        :param volume: :obj:`int` desired audio volume (0 - 100%)
        """
        self.test_action(PFxAction().set_volume(volume))

    def refresh_file_dir(self):
        """
        Reads the PFx Brick file system directory. This includes
        the total storage used as well as the remaining capacity.
        Individual file directory entries are stored in the
        :obj:`PFxBrick.filedir.files` class variable.
        """
        res = cmd_get_free_space(self.dev)
        if res:
            self.filedir.bytesLeft = uint32_toint(res[3:7])
            capacity = uint32_toint(res[7:11])
            self.filedir.bytesUsed = capacity - self.filedir.bytesLeft
        res = cmd_get_num_files(self.dev)
        if res:
            self.filedir.files = []
            self.filedir.numFiles = uint16_toint(res[3:5])
            file_count = 0
            for i in range(PFX_AUDIO_FILES_MAX):
                res = cmd_get_dir_entry(self.dev, i + 1)
                d = PFxFile()
                d.from_bytes(res)
                if d.id < 0xFF:
                    self.filedir.files.append(d)
                    file_count += 1
                if file_count >= self.filedir.numFiles:
                    break

    def put_file(self, fn, fileID=None, show_progress=True):
        """
        Copies a file from the host to the PFx Brick.

        :param fn: :obj:`str` the filename (optionally including the path) of the file to copy
        :param fileID: :obj:`int` the unique file ID to assign the copied file in the file system, can be None for automatic assignment
        :param show_progress: :obj:`boolean` a flag to show the progress bar indicator during transfer.
        """
        if fileID is None:
            self.refresh_file_dir()
            fileID = self.filedir.find_available_file_id()
        if fileID is not None:
            fs_copy_file_to(self, fileID, fn, show_progress)

    def get_file(self, fileID, fn=None, show_progress=True):
        """
        Copies a file from the PFx Brick to the host.

        :param fileID: :obj:`int` or :obj:`str` the file ID or filename of the file to copy
        :param fn: :obj:`str` optional override for the filename when copied into the host
        :param show_progress: :obj:`boolean` a flag to show the progress bar indicator during transfer.
        """
        self.refresh_file_dir()
        fileID = self.file_id_from_str_or_int(fileID)
        f = self.filedir.get_file_dir_entry(fileID)
        fs_copy_file_from(self, f, fn, show_progress)

    def remove_file(self, fileID, silent=False):
        """
        Removes a file from the PFx Brick file system.

        :param fileID: :obj:`int` or :obj:`str` the file ID or filename of the file to remove
        :param silent: :obj:`boolean` if True, warnings about missing files are suppressed
        """
        fileID = self.file_id_from_str_or_int(fileID)
        fs_remove_file(self.dev, fileID, silent=silent)

    def format_fs(self, quick=False):
        """
        Formats the PFx Brick file system, erasing all files.

        :param quick: :obj:`boolean` If True, only occupied sectors are erased. If False, every sector is erased, i.e. a complete format.
        """
        fs_format(self.dev, quick)

    def set_file_attributes(self, fileID, attr, mask=0x7C):
        """
        Sets the upper 8-bit attribute field of a file's directory entry.

        Although the file attribute field is actually 16 bits, this function sets the upper
        8 bits.  The lower 8-bits are reserved for identifying the file type, e.g. text, WAV,
        etc.

        :param fileID: :obj:`int` or :obj:`str` the file ID or filename of the file to remove
        :param attr: :obj:`int` the attribute value to set (only the lower 16)
        :param mask: :obj:`int` an optional bit mask applied to the attributes
        """
        fileID = self.file_id_from_str_or_int(fileID)
        attr = attr & 0xFF
        res = self.send_raw_icd_command(
            [
                PFX_CMD_FILE_DIR,
                PFX_DIR_REQ_SET_ATTR_MASKED_ID,
                fileID & 0xFF,
                0x00,
                attr,
                0x00,
                mask,
            ]
        )

    def rename_file(self, fileID, new_name):
        """
        Renames a file on the file system.

        :param fileID: :obj:`int` or :obj:`str` the file ID or filename of the file to rename
        :param new_name: :obj:`str` new file name to apply (up to 32 characters UTF-8 encoded)
        """
        fileID = self.file_id_from_str_or_int(fileID)
        mb = bytes(new_name, "utf-8")
        name_len = min(len(mb), 32)
        mb = mb[:name_len]
        res = self.send_raw_icd_command(
            [
                PFX_CMD_FILE_DIR,
                PFX_DIR_REQ_RENAME_FILE_ID,
                fileID & 0xFF,
                *mb,
            ]
        )

    def stop_script(self):
        """
        Stops all script execution.
        """
        res = cmd_run_script(self.dev, 0xFF)

    def run_script(self, scriptfile):
        """
        Runs a specified script file on the PFx Brick filesystem.

        A file is identified either by its numeric file ID (0 - 254) or alphanumeric
        filename as a string.

        :param scriptfile: :obj:`int` or :obj:`str` file ID or file name string
        """
        fileID = self.file_id_from_str_or_int(scriptfile)
        res = cmd_run_script(self.dev, fileID)

    def file_id_from_str_or_int(self, filespec):
        """
        Returns a numeric file ID from either a string filename or integer file ID.

        A file is identified on the PFx Brick filesystem primarily by its numeric
        file ID (0 - 254).  A file ID of 255 is an invalid or non-existant file.
        A numeric file ID can be queried using its alphanumeric filename in the
        filesystem directory.  This function performs this lookup if necessary,
        i.e. if a string filename is provided.

        :param filespec: :obj:`int` or :obj:`str` file ID or file name string
        :returns: :obj:`int` numeric file ID from PFx Brick filesystem, or 0xFF if not found
        """
        if isinstance(filespec, int):
            return filespec
        elif isinstance(filespec, str):
            fileid = fs_get_fileid_from_name(self.dev, filespec)
            return fileid
        return 0xFF

    def get_current_state(self):
        """
        Returns the current state of the PFx Brick operating parameters.

        :returns: :obj:`PFxState` a dataclass container with state information
        """
        res = cmd_get_current_state(self.dev)
        self.state.from_bytes(res)
        return self.state

    def get_fs_state(self):
        """
        Returns the current state of the PFx Brick file system.

        :returns: :obj:`PFxFSState` a dataclass container of file system information
        """
        res = self.send_raw_icd_command([PFX_CMD_FILE_GET_FS_STATE])
        self.state.filesys.from_bytes(res)
        return self.state.filesys

    def get_bt_state(self):
        """
        Returns the current state of the PFx Brick Bluetooth radio module.

        :returns: :obj:`PFxBTState` a dataclass container of Bluetooth module information
        """
        res = self.send_raw_icd_command([PFX_CMD_GET_BT_STATUS])
        self.state.bt.from_bytes(res)
        return self.state.bt

    def send_raw_icd_command(self, msg):
        """
        Sends a raw ICD command message represented as a list of bytes.

        :returns: :obj:`bytes` response from the PFx Brick
        """
        res = cmd_raw(self.dev, msg)
        return res
