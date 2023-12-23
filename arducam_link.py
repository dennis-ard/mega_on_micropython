    
from machine import UART, Pin

from arducam_mega import *

class arducam_link:
    RESET_CAMERA                = 0xFF
    SET_PICTURE_RESOLUTION      = 0x01
    SET_VIDEO_RESOLUTION        = 0x02
    SET_BRIGHTNESS              = 0x03
    SET_CONTRAST                = 0x04
    SET_SATURATION              = 0x05
    SET_EV                      = 0x06
    SET_WHITEBALANCE            = 0x07
    SET_SPECIAL_EFFECTS         = 0x08
    SET_FOCUS_ENABEL            = 0x09
    SET_EXPOSUREANDGAIN_ENABEL  = 0x0A
    SET_WHILEBALANCE_ENABEL     = 0x0C
    SET_MANUAL_GAIN             = 0x0D
    SET_MANUAL_EXPOSURE         = 0x0E
    GET_CAMERA_INFO             = 0x0F
    TAKE_PICTURE                = 0x10
    SET_SHARPNESS               = 0x11
    DEBUG_WRITE_REGISTER        = 0x12
    STOP_STREAM                 = 0x21
    GET_FRM_VER_INFO            = 0x30
    GET_SDK_VER_INFO            = 0x40
    SET_IMAGE_QUALITY           = 0x50
    SET_LOWPOWER_MODE           = 0x60
    
    pack_head = bytearray(b'\xff\xaa\x00\xff\xbb')

    def __init__(self, pin) -> None:
        self.uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
        self.CAM = arducam_mega(pin)
        self.recv_state = 0x00
        self.recv_cmdline = []
        self.preivew_on = False
    def read(self):
        return self.uart.read(1)
    
    def send(self, buf):
        self.uart.write(buf)
    
    def pack_send(self, pack_type, buf):
        buf_len = len(buf).to_bytes(4, 'little')
        self.pack_head[2] = pack_type
        self.send(self.pack_head[0:3])
        self.send(buf_len)
        self.send(buf)
        self.send(self.pack_head[3:])
        
    def process(self, cmdline):
        if cmdline[0] == self.SET_PICTURE_RESOLUTION:
            self.set_mega_resolution(cmdline[1])
        elif cmdline[0] == self.SET_VIDEO_RESOLUTION:
            self.preivew_on = True
            self.video_len = 0
            self.set_mega_resolution(cmdline[1]|0x10)
        elif cmdline[0] == self.SET_BRIGHTNESS:
            self.CAM.set_brightness(cmdline[1])
        elif cmdline[0] == self.SET_CONTRAST:
            self.CAM.set_contrast(cmdline[1])
        elif cmdline[0] == self.SET_SATURATION:
            self.CAM.set_saturation(cmdline[1])
        elif cmdline[0] == self.SET_EV:
            self.CAM.set_EV(cmdline[1])
        elif cmdline[0] == self.SET_WHITEBALANCE:
            self.CAM.set_white_bal(cmdline[1])
        elif cmdline[0] == self.SET_SPECIAL_EFFECTS:
            self.CAM.set_special_effects(cmdline[1])
        # if cmdline[0] == SET_FOCUS_CONTROL: // Focus Control
        #     setAutoFocus(camera, cmdline[1])
        #     if (cmdline[1] == 0) {
        #         setAutoFocus(camera, 0x02)
        #     }
        elif cmdline[0] == self.SET_EXPOSUREANDGAIN_ENABEL:
            self.CAM.set_exposure_enable(cmdline[1])
            self.CAM.set_gain_enable(cmdline[1])
        elif cmdline[0] == self.SET_WHILEBALANCE_ENABEL:
            self.CAM.set_white_bal_enable(cmdline[1])
        elif cmdline[0] == self.SET_SHARPNESS:
            self.CAM.set_sharpness(cmdline[1])
        elif cmdline[0] == self.SET_MANUAL_GAIN:
            gain_value = (cmdline[1]<<8) | cmdline[2]
            self.CAM.set_gain(gain_value)
        elif cmdline[0] == self.SET_MANUAL_EXPOSURE: 
            exposure_value = (cmdline[1] << 16) | (cmdline[2] << 8) | cmdline[3]
            self.CAM.set_exposure(exposure_value)
        elif cmdline[0] == self.GET_CAMERA_INFO:
            self.report_mega_info()
        elif cmdline[0] == self.TAKE_PICTURE:
            self.take_picture() 
        elif cmdline[0] == self.STOP_STREAM:
            self.preivew_on = False
            self.send(self.pack_head[3:])
        # if cmdline[0] == GET_FRM_VER_INFO: // Get Firmware version info
        #     reportVerInfo(camera)
        #     break
        # if cmdline[0] == GET_SDK_VER_INFO: // Get sdk version info
        #     reportSdkVerInfo(camera)
        #     break
        elif cmdline[0] == self.RESET_CAMERA:
            self.CAM.soft_reset()
            self.CAM.check_connection()
        elif cmdline[0] == self.SET_IMAGE_QUALITY:
            self.CAM.set_JPEG_quality(cmdline[1])
        elif cmdline[0] == self.SET_LOWPOWER_MODE:
            self.CAM.set_lowpower_enable(cmdline[1])
        else:
            pass
        return cmdline[0]
    
    def report_mega_info(self):
        if self.CAM.camera_id == MEGA_CAEMRA._3MP_1 or self.CAM.camera_id == MEGA_CAEMRA._3MP_2:
            mega_name = '3MP'
        elif self.CAM.camera_id == MEGA_CAEMRA._5MP_1:
            mega_name = '5MP'
        elif self.CAM.camera_id == MEGA_CAEMRA._5MP_2:
            mega_name = '5MP_2'
        else:
            return 
        str_buf = "ReportCameraInfo\r\nCamera Type: {}\r\nCamera Support Resolution: {}\r\nCamera Support specialeffects: {}\r\nCamera Support Focus: {}\r\nCamera Exposure Value Max: {}\r\nCamera Exposure Value Min: {}\r\nCamera Gain Value Max: {}\r\nCamera Gain Value Min: {}\r\nCamera Support Sharpness: {}".format(
            mega_name,
            self.CAM.camera_info.s_resoultion,
            self.CAM.camera_info.s_special_effects,
            self.CAM.camera_info.e_focus,
            self.CAM.camera_info.exposure_max,
            self.CAM.camera_info.exposure_min,
            self.CAM.camera_info.gain_max,
            self.CAM.camera_info.gain_min,
            self.CAM.camera_info.e_sharpness
        )
        self.pack_send(0x02, str_buf)
    
    def take_picture(self):
        frame_len = self.CAM.capture()
        start_flag = True
        if frame_len > 0:
            buf_len = frame_len.to_bytes(4, 'little')
            self.pack_head[2] = 0x01
            self.send(self.pack_head[0:3])
            self.send(buf_len)
            self.send(((self.CAM.current_resolution << 4) | 0x01).to_bytes(1, 'little'))
            while frame_len > 0 :
                read_len = 1024 if frame_len > 1024 else frame_len
                buf = self.CAM.read_fifo(read_len,start_flag)
                self.send(buf)
                frame_len -= len(buf)
                start_flag = False
            self.send(self.pack_head[3:])
    
    def video_preivew(self):
        if self.preivew_on :
            if self.video_len > 1024:
                buf = self.CAM.read_fifo(1024)
                self.send(buf)
                self.video_len -= 1024
            elif self.video_len > 0:
                buf = self.CAM.read_fifo(self.video_len)
                self.send(buf)
                self.video_len = 0
                self.send(self.pack_head[3:])
            else :
                self.video_len = self.CAM.capture()
                self.pack_head[2] = 0x01
                self.send(self.pack_head[0:3])
                self.send(self.video_len.to_bytes(4, 'little'))
                self.send(((self.CAM.current_resolution << 4) | 0x01).to_bytes(1, 'little'))
                if self.video_len > 1024:
                    recv_buf = 1024
                else:
                    recv_buf = self.video_len
                buf = self.CAM.read_fifo(recv_buf,True)
                self.send(buf)
                self.video_len -= recv_buf

    def run(self):
        if self.uart.any():
            recv_buf = bytearray(self.uart.read())
            # print(recv_buf)
            for item in recv_buf:
                if self.recv_state == 0x00:
                    if item == 0x55:
                        self.recv_state = 0x01
                        self.recv_cmdline.clear()
                elif self.recv_state == 0x01:
                    if item == 0xaa:
                        self.process(self.recv_cmdline)
                        self.recv_state = 0x00
                        return
                    else:
                        self.recv_cmdline.append(item)
                        if len(self.recv_cmdline) > 7:
                            self.recv_state = 0x00
                            return
        self.video_preivew()
                        
    def set_mega_resolution(self, fmt):
        return self.CAM.set_fmt(fmt>>0x04, fmt&0x0f)
         
if __name__ == "__main__":
    Link = arducam_link(17)
    while 1:
        Link.run()