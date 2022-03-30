class GameStats():
    def __init__(self,ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()

        #让游戏开始处于一个非活动状态
        self.game_active = False
        #在任何情况下都不应重置最高分
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        """初始化在游戏运行期间可能发生变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0