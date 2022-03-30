import sys,pygame
from bullets import Bullet
from alien import Alien
from time import sleep
#将函数封装在一个特定的模块之中

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):  #事件管理函数，在编写某一特定的函数时，一定要赋予其参数
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN: #检测按键按下，则将值改为true
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP: #检测按键抬起，则将值改为false
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x , mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,
                              bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,
                      bullets,mouse_x,mouse_y):
    """在玩家单击play按钮的时候开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active: #检查鼠标单击时是否在play按钮内
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #清空外星人列表和子弹列表
        bullets.empty()
        aliens.empty()

        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #使用函数时，一定要注意传递需要的参数
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    #如果游戏处于非活动状态，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,bullets,aliens):
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    #检查是否有子弹击中了外星人
    #如果是这样就删除相应的子弹和外星人
    check_bullet_alien_collisons(ai_settings, screen, stats,sb,ship, aliens, bullets)

def check_bullet_alien_collisons(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """响应子弹与外星人的碰撞"""
    #删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        #提高等级
        stats.level += 1
        sb.prep_level()
        #生成新的外星人群
        create_fleet(ai_settings, screen, ship, aliens)

def update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets):
    """检查是否有外星人到达屏幕的边缘，然后更新所有的外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    #检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings, stats, screen, sb,ship, aliens, bullets)
    #检查是否有外星人到达底部
    check_aliens_bottom(ai_settings, stats, screen,sb,ship,aliens, bullets)

def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets) <= ai_settings.bullets_allowed:
        """如果还没有到达限制，就发射一枚子弹"""
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_alien_x(ai_settings,alien_width):
    """计算每行可以容纳多少外星人"""
    avaliable_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可以容纳多少外星人"""
    avaliable_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(avaliable_space_y/(2 * alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人，并把其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.x
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    #创建一个外星人，并计算一行可以容纳多少个外星人
    #外星人间距为外星人宽度
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_alien_x(ai_settings , alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    #创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
        #创建一个外星人加入当前行
            create_alien(ai_settings, screen, aliens, alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    for aline in aliens:
        aline.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets):
    """响应被外星人撞到的飞船"""
    #将ship_left减一
    if stats.ships_left > 0:
        stats.ships_left -= 1

        #更新记分牌
        sb.prep_ships()

    #清空子弹和外星人列表
        bullets.empty()
        aliens.empty()

    #创建新的飞船，并将飞船放到屏幕底部的中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
    #暂停0.5秒
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets):
    """检查是否有外星人到达了底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞一样做出处理
            ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
            break

def check_high_score(stats,sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

