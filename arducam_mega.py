from machine import Pin, SPI
import time

class MEGA_COMMON:
    ARDUCHIP_FIFO = 0x04
    ARDUCHIP_FIFO_2 = 0x07

    FIFO_CLEAR_ID_MASK = 0x01
    FIFO_START_MASK = 0x02

    ARDUCHIP_TRIG = 0x44
    VSYNC_MASK = 0x01
    SHUTTER_MASK = 0x02
    CAP_DONE_MASK = 0x04

    FIFO_SIZE1 = 0x45
    FIFO_SIZE2 = 0x46
    FIFO_SIZE3 = 0x47

    BURST_FIFO_READ = 0x3C
    SINGLE_FIFO_READ = 0x3D

    CAM_REG_POWER_CONTROL = 0x02
    CAM_REG_SENSOR_RESET = 0x07
    CAM_REG_FORMAT = 0x20
    CAM_REG_CAPTURE_RESOLUTION = 0x21
    CAM_REG_BRIGHTNESS_CONTROL = 0x22
    CAM_REG_CONTRAST_CONTROL = 0x23
    CAM_REG_SATURATION_CONTROL = 0x24
    CAM_REG_EV_CONTROL = 0x25
    CAM_REG_WHILEBALANCE_CONTROL = 0x26
    CAM_REG_COLOR_EFFECT_CONTROL = 0x27
    CAM_REG_SHARPNESS_CONTROL = 0x28
    CAM_REG_AUTO_FOCUS_CONTROL = 0x29
    CAM_REG_IMAGE_QUALITY = 0x2A
    CAM_REG_EXPOSURE_GAIN_WHILEBAL_ENABLE = 0x30
    CAM_REG_MANUAL_GAIN_BIT_9_8 = 0x31
    CAM_REG_MANUAL_GAIN_BIT_7_0 = 0x32
    CAM_REG_MANUAL_EXPOSURE_BIT_19_16 = 0x33
    CAM_REG_MANUAL_EXPOSURE_BIT_15_8 = 0x34
    CAM_REG_MANUAL_EXPOSURE_BIT_7_0 = 0x35
    CAM_REG_BURST_FIFO_READ_OPERATION = 0x3C
    CAM_REG_SINGLE_FIFO_READ_OPERATION = 0x3D
    CAM_REG_SENSOR_ID = 0x40
    CAM_REG_YEAR_SDK = 0x41
    CAM_REG_MONTH_SDK = 0x42
    CAM_REG_DAY_SDK = 0x43
    CAM_REG_SENSOR_STATE = 0x44
    CAM_REG_FPGA_VERSION_NUMBER = 0x49
    CAM_REG_DEBUG_DEVICE_ADDRESS = 0x0A
    CAM_REG_DEBUG_REGISTER_HIGH = 0x0B
    CAM_REG_DEBUG_REGISTER_LOW = 0x0C
    CAM_REG_DEBUG_REGISTER_VALUE = 0x0D

    SENSOR_STATE_IDLE = 1 << 1
    SENSOR_RESET_ENABLE = 1 << 6

    CTR_WHILEBALANCE = 0x02
    CTR_EXPOSURE = 0x01
    CTR_GAIN = 0x00

class MEGA_CONTRAST_LEVEL:
    NEGATIVE_3 = 6
    NEGATIVE_2 = 4
    NEGATIVE_1 = 2
    DEFAULT = 0
    _1 = 1
    _2 = 3
    _3 = 5

class MEGA_EV_LEVEL:
    NEGATIVE_3 = 6
    NEGATIVE_2 = 4
    NEGATIVE_1 = 2
    DEFAULT = 0
    _1 = 1
    _2 = 3
    _3 = 5

class MEGA_STAURATION_LEVEL:
    NEGATIVE_3 = 6
    NEGATIVE_2 = 4
    NEGATIVE_1 = 2
    DEFAULT = 0
    _1 = 1
    _2 = 3
    _3 = 5

class MEGA_BRIGHTNESS_LEVEL:
    NEGATIVE_4 = 8
    NEGATIVE_3 = 6
    NEGATIVE_2 = 4
    NEGATIVE_1 = 2
    DEFAULT = 0
    _1 = 1
    _2 = 3
    _3 = 5
    _4 = 7

class MEGA_SHARPNESS_LEVEL:
    AUTO = 0
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6
    _7 = 7
    _8 = 8

class MEGA_COLOR_FX:
    NONE = 0
    BLUEISH = 1
    REDISH = 2
    BW = 3
    SEPIA = 4
    NEGATIVE = 5
    GRASS_GREEN = 6
    OVER_EXPOSURE = 7
    SOLARIZE = 8

class MEGA_WHITE_BALANCE:
    DEFAULT = 0
    SUNNY = 1
    OFFICE = 2
    CLOUDY = 3
    HOME = 4

class MEGA_IMAGE_QUALITY:
    HIGH_QUALITY = 0
    DEFAULT_QUALITY = 1
    LOW_QUALITY = 2

class MEGA_CAEMRA:
    _5MP_1 = 0x81
    _3MP_1 = 0x82
    _5MP_2 = 0x83
    _3MP_2 = 0x84

class MEGA_RESOLUTION:
    QQVGA = 0x00     # 160x120
    QVGA = 0x01      # 320x240
    VGA = 0x02       # 640x480
    SVGA = 0x03      # 800x600
    HD = 0x04        # 1280x720
    SXGAM = 0x05     # 1280x960
    UXGA = 0x06      # 1600x1200
    FHD = 0x07       # 1920x1080
    QXGA = 0x08      # 2048x1536
    WQXGA2 = 0x09    # 2592x1944
    _96X96 = 0x0a    # 96x96
    _128X128 = 0x0b  # 128x128
    _320X320 = 0x0c  # 320x320
    _12 = 0x0d       # Reserve
    _13 = 0x0e       # Reserve
    _14 = 0x0f       # Reserve
    _15 = 0x10       # Reserve
    NONE = -1

class MEGA_PIXELFORMAT:
    JPEG = 0x01
    RGB565 = 0x02
    YUV = 0x03
    NONE = -1

class arducam_mega:
    class mega_info:
        def __init__(self, s_resolution, s_special_effects, exposure_max, exposure_min, gain_max, gain_min, e_focus,e_sharpness,device_addr) -> None:
            self.s_resolution = s_resolution
            self.s_special_effects = s_special_effects
            self.exposure_max = exposure_max
            self.exposure_min = exposure_min
            self.gain_max = gain_max
            self.gain_min = gain_min
            self.e_focus = e_focus
            self.e_sharpness = e_sharpness
            self.device_addr = device_addr
            
    support_resolution = [
        MEGA_RESOLUTION._96X96,
        MEGA_RESOLUTION._128X128,
        MEGA_RESOLUTION.QVGA,
        MEGA_RESOLUTION._320X320,
        MEGA_RESOLUTION.VGA,
        MEGA_RESOLUTION.HD,
        MEGA_RESOLUTION.UXGA,
        MEGA_RESOLUTION.FHD,
        MEGA_RESOLUTION.NONE,
    ]
    
    def __init__(self, nss: int) -> None:
        self.spi = SPI(0, 4_000_000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
        self.nss = Pin(nss, Pin.OUT, value=1)
        self.camera_id = 0x0
        self.current_pixelfmt = MEGA_PIXELFORMAT.NONE
        self.current_resolution = MEGA_RESOLUTION.NONE
        self.camera_info = None
    def reg_write(self, reg: int, val: int):
        try: 
            self.nss(0)
            reg |= 0x80
            tx_buf = reg.to_bytes(1,'little') + val.to_bytes(1,'little')
            self.spi.write(tx_buf)
        finally:
            self.nss(1)
        # print(tx_buf)
        
    def reg_read(self, reg):
        try:
            reg &= 0x7f
            self.nss(0)
            buf = bytearray(3)
            self.spi.readinto(buf,reg)
        finally:
            self.nss(1)
        return buf[2]
    
    def await_bus_idle(self, tries):
        while (self.reg_read(MEGA_COMMON.CAM_REG_SENSOR_STATE) & 0x03) != MEGA_COMMON.SENSOR_STATE_IDLE :
            tries -= 1
            if tries <= 0:
                return -1
            time.sleep_ms(2)
        return 0 
    
    def check_connection(self):
        ret = self.await_bus_idle(500)
        self.camera_id = self.reg_read(MEGA_COMMON.CAM_REG_SENSOR_ID)
        print("detect camera id: ",self.camera_id)
        if self.camera_id == MEGA_CAEMRA._3MP_1 or self.camera_id == MEGA_CAEMRA._3MP_2:
            self.support_resolution[8] = MEGA_RESOLUTION.QXGA
            self.camera_info = self.mega_info(s_resolution=7638,s_special_effects=319,exposure_max=30000,exposure_min=1,gain_max=1023,gain_min=1,e_focus=0,e_sharpness=1,device_addr=0x78)
        elif self.camera_id == MEGA_CAEMRA._5MP_1 or self.camera_id == MEGA_CAEMRA._5MP_2:
            self.support_resolution[8] = MEGA_RESOLUTION.WQXGA2
            self.camera_info = self.mega_info(s_resolution=7894,s_special_effects=63,exposure_max=30000,exposure_min=1,gain_max=1023,gain_min=1,e_focus=1,e_sharpness=0,device_addr=0x78)
        else:
            print("No camera found!")
            return -1
        return ret 
    
    def set_resolution(self, resolution):
        ret = self.await_bus_idle(3)
        self.reg_write(MEGA_COMMON.CAM_REG_CAPTURE_RESOLUTION, resolution)
        ret |= self.await_bus_idle(10)
        
        if ret == 0 :
            self.current_resolution = resolution
        
        return ret
    
    def set_pixeformat(self, pixeformat):
        ret = self.await_bus_idle(3)
        self.reg_write(MEGA_COMMON.CAM_REG_FORMAT, pixeformat)
        ret |= self.await_bus_idle(10)
        
        if ret == 0 :
            self.current_pixelfmt = pixeformat
        
        return ret
    
    def capture(self):
        self.reg_write(MEGA_COMMON.ARDUCHIP_FIFO, MEGA_COMMON.FIFO_CLEAR_ID_MASK)
        self.reg_write(MEGA_COMMON.ARDUCHIP_FIFO, MEGA_COMMON.FIFO_START_MASK)
        tries = 200
        fifo_len = 0
        while tries > 0:
            time.sleep_ms(2)
            if self.reg_read(MEGA_COMMON.ARDUCHIP_TRIG) & MEGA_COMMON.CAP_DONE_MASK:
                break
            tries -= 1
        if tries <= 0:
            return -1
        fifo_len = self.reg_read(MEGA_COMMON.FIFO_SIZE1)
        fifo_len |= self.reg_read(MEGA_COMMON.FIFO_SIZE2) << 8
        fifo_len |= self.reg_read(MEGA_COMMON.FIFO_SIZE3) << 16
        return fifo_len
    
    def read_fifo(self, len, head_flag=False):
        try:
            self.nss(0)
            if head_flag:
                self.spi.read(2,MEGA_COMMON.BURST_FIFO_READ)
            else:
                self.spi.read(1,MEGA_COMMON.BURST_FIFO_READ)
                
            buf = bytearray(len)
            self.spi.readinto(buf)
        finally:
            self.nss(1)
        return buf

    def soft_reset(self):
        self.reg_write(MEGA_COMMON.CAM_REG_SENSOR_RESET, MEGA_COMMON.SENSOR_RESET_ENABLE)
        time.sleep_ms(1000)
    
    def set_brightness(self, level):
        ret = self.await_bus_idle(3)
        self.reg_write(MEGA_COMMON.CAM_REG_BRIGHTNESS_CONTROL, level)
        ret |= self.await_bus_idle(10)
        return ret
    
    def set_saturation(self, level):
        ret = self.await_bus_idle(3)
        self.reg_write(MEGA_COMMON.CAM_REG_SATURATION_CONTROL, level)
        ret |= self.await_bus_idle(10)
        return ret
    
    def set_contrast(self, level):
        ret = self.await_bus_idle(3)
        self.reg_write(MEGA_COMMON.CAM_REG_CONTRAST_CONTROL, level)
        ret |= self.await_bus_idle(10)
        return ret
    
    def set_EV(self, level):
        ret = self.await_bus_idle(3)
        self.reg_write(MEGA_COMMON.CAM_REG_EV_CONTROL, level)
        ret |= self.await_bus_idle(10)
        return ret
    
    def set_sharpness(self, level):
        if self.enable_sharpness == 0:
            return -1
        ret = self.await_bus_idle(3)
        self.reg_write(MEGA_COMMON.CAM_REG_SHARPNESS_CONTROL, level)
        ret |= self.await_bus_idle(10)
        return ret
    
    def set_special_effects(self, effect):
        ret = self.await_bus_idle(3)
        self.reg_write(MEGA_COMMON.CAM_REG_COLOR_EFFECT_CONTROL, effect)
        ret |= self.await_bus_idle(10)
        return ret
    
    def set_JPEG_quality(self, qs):
        if self.current_pixelfmt != MEGA_PIXELFORMAT.JPEG:
            return -1
        ret = self.await_bus_idle(3)
        self.reg_write(MEGA_COMMON.CAM_REG_IMAGE_QUALITY, qs)
        ret |= self.await_bus_idle(10)
        return ret
    
    def set_white_bal_enable(self, enable):
        reg = 0x80 if enable else 0
        reg |= MEGA_COMMON.CTR_WHILEBALANCE
        ret = self.await_bus_idle(3)
        self.reg_write(MEGA_COMMON.CAM_REG_EXPOSURE_GAIN_WHILEBAL_ENABLE, reg)
        ret |= self.await_bus_idle(10)
        return ret

    def set_white_bal(self, level):
        ret = self.await_bus_idle(3)
        self.reg_write(MEGA_COMMON.CAM_REG_WHILEBALANCE_CONTROL, level)
        ret |= self.await_bus_idle(10)
        return ret
    
    def set_gain_enable(self, enable):
        reg = 0x80 if enable else 0
        reg |= MEGA_COMMON.CTR_GAIN
        ret = self.await_bus_idle(3)
        self.reg_write(MEGA_COMMON.CAM_REG_EXPOSURE_GAIN_WHILEBAL_ENABLE, reg)
        ret |= self.await_bus_idle(10)
        
    def set_gain(self, value):
        ret = self.await_bus_idle(3)
        self.reg_write(MEGA_COMMON.CAM_REG_MANUAL_GAIN_BIT_9_8, (value >> 8) & 0xff)
        ret |= self.await_bus_idle(10)
        self.reg_write(MEGA_COMMON.CAM_REG_MANUAL_GAIN_BIT_7_0, value & 0xff)
        ret |= self.await_bus_idle(10)
        return ret
    
    def set_exposure_enable(self, enable):
        reg = 0x80 if enable else 0
        reg |= MEGA_COMMON.CTR_EXPOSURE
        ret = self.await_bus_idle(3)
        self.reg_write(MEGA_COMMON.CAM_REG_EXPOSURE_GAIN_WHILEBAL_ENABLE, reg)
        ret |= self.await_bus_idle(10)
    
    def set_exposure(self, value):
        ret = self.await_bus_idle(3)
        self.reg_write(MEGA_COMMON.CAM_REG_MANUAL_EXPOSURE_BIT_19_16, (value >> 16) & 0xff)
        ret |= self.await_bus_idle(10)
        self.reg_write(MEGA_COMMON.CAM_REG_MANUAL_EXPOSURE_BIT_15_8, (value >> 8) & 0xff)
        ret |= self.await_bus_idle(10)
        self.reg_write(MEGA_COMMON.CAM_REG_MANUAL_EXPOSURE_BIT_7_0, value & 0xff)
        ret |= self.await_bus_idle(10)
        return ret
    
    def set_lowpower_enable(self, enable):
        if self.camera_id == MEGA_CAEMRA._3MP_2 or self.camera_id == MEGA_CAEMRA._5MP_2:
            enable != enable
        if enable:
            self.reg_write(MEGA_COMMON.CAM_REG_POWER_CONTROL,0x07)
        else:
            self.reg_write(MEGA_COMMON.CAM_REG_POWER_CONTROL,0x05)
    
    def set_fmt(self, pixefmt, resolution):
        if pixefmt == self.current_pixelfmt and resolution == self.current_resolution:
            return 0
        
        if pixefmt in [0x00, 0x01, 0x02]:
            ret = self.set_pixeformat(pixefmt)
        else:
            return -1
        
        if resolution in self.support_resolution:
            ret |= self.set_resolution(resolution)
        else:
            return -1
        return ret
    
if __name__ == "__main__":
    CAM = arducam_mega(17)
    CAM.soft_reset()
    CAM.check_connection()
    CAM.set_fmt(MEGA_PIXELFORMAT.JPEG, MEGA_RESOLUTION._96X96)
    frame_len = CAM.capture()
    start_flag = True
    if frame_len > 0:
        while frame_len > 0 :
            read_len = 1024 if frame_len > 1024 else frame_len
            buf = CAM.read_fifo(read_len,start_flag)
            print(buf)
            frame_len -= len(buf)
            start_flag = False
