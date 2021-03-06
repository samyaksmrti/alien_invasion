class Settings:   #将游戏所需要的设置及参数封装在一个模块之中，然后在主文件之中对模块进行调用

    def __init__(self):
        """初始化游戏的设置"""
        #屏幕设置以及背景颜色
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230,230,230)

        self.ship_speed_factor = 1.5 #飞船速度
        #settings of bullet
        self.bullet_speed_factor = 1
        self.bullet_color = 60,60,60
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullets_allowed = 3
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        #fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1
        self.ship_limit = 3
        #以什么样的速度加快游戏节奏
        self.speed_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        #fleet_direction为1表示向右，-1表示向左
        self.fleet_direction = 1
        #计分
        self.alien_points = 50

    def increase_speed(self):
        #提高速度设置
        self.ship_speed_factor *= self.speed_scale
        self.alien_speed_factor *= self.speed_scale
        self.bullet_speed_factor *= self.speed_scale
        self.alien_points  = int(self.alien_points * self.score_scale)
        print(self.alien_points) #打印出最新的点数值



