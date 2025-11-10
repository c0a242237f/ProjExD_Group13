import pygame as pg
import os
import sys
import random
import math
import time

#ーーーーーーーーーーー初期設定(定数など)ーーーーーーーーーーー
os.chdir(os.path.dirname(os.path.abspath(__file__)))
#ステージ関係
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 # 画面のサイズ
LEFT_BOUND, RIGHT_BOUND = SCREEN_WIDTH // 3, SCREEN_WIDTH * 2 // 4 # スクロール判定
TILE_SIZE_X, TILE_SIZE_Y = 100, 40 # タイルのサイズ
ADD_STAGE_BLOCK = 50 # ステージの拡張幅

#共通の挙動
GRAVITY = 0.8         # 重力
NO_DAMAGE_TIME = 120 # 無敵時間(フレーム単位)

#プレイヤー挙動
PLAYER_SPEED = 10      # 左右の移動速度
PLAYER_HP = 5
JUMP_STRENGTH = -15   # ジャンプ力 (Y軸は上がマイナス)
HOVER_AIR_TIME = 60   # ホバーエフェクトの表示時間(フレーム単位)
BULLET_SPEED = 10 # カジノ状態の弾の速度
BOMB_FUSE_TIME = 3.0  # 爆弾の導火線の時間(秒)
BOMB_EXPLOSION_DURATION = 120  # 爆発エフェクトの表示時間(フレーム単位)
BOMB_RADIUS = TILE_SIZE_X * 1  # 爆発範囲の半径

#敵の挙動
ENEMY_SPEED = 1
ENEMY_NUM = 3 # 敵の数

#ーーーーーーーーーーーー関数の宣言ーーーーーーーーーーーーーー  
#画面設定
def start_page(screen: pg.surface, clock: pg.time.Clock) -> int:
    """
    スタート画面を表示する関数
    引数: スクリーンsurface, pgのクロック  
    戻り値: int(開始なら0, 終了なら-1)
    """
    bg_img = pg.image.load("fig/night_plain_bg.png") # 背景画像
    title = Text("GO KOUKATON (TUT)", 80, (100, 300))
    start_button = Text("Start", 80, (100, 100))
    end_button = Text("Quit", 80, (500, 100))
    credit = Text("BGM: 魔王魂", 20, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 50), "ja")

    mouse_x, mouse_y = -1000, -1000 # マウス位置をあり得ない位置で初期化
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return -1
        
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos # マウスの位置を取得
 
        screen.blit(bg_img, (0, 0))
        screen.blit(title.txt, (title.x, title.y))
        screen.blit(start_button.txt, (start_button.x, start_button.y))
        screen.blit(end_button.txt, (end_button.x, end_button.y))
        screen.blit(credit.txt, (credit.x, credit.y))
        
        
        if start_button.x < mouse_x < start_button.x + start_button.width and end_button.y < mouse_y < end_button.y + end_button.height:
            return 0 # スタートボタンをクリック
        if end_button.x < mouse_x < end_button.x + end_button.width and end_button.y < mouse_y < end_button.y + end_button.height:
            return -1 # 終了ボタンをクリック
                
        pg.display.update()
        clock.tick(60)


def gameover(screen: pg.surface, clock: pg.time.Clock) -> int:
    """
    ゲームオーバー画面を表示する関数
    引数: スクリーンsurface, pgのクロック
    戻り値: int(開始なら0, 終了なら-1)    
    """
    bg_img = pg.image.load("fig/night_plain_bg.png") # 背景画像
    txt = Text("Game Over", 80, (100, 300))
    retry = Text("Retry", 80, (100, 100))
    quit = Text("Quit", 80, (500, 100))

    mouse_x, mouse_y = -1000, -1000 # マウス位置をあり得ない位置で初期化

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return -1
        
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos # マウス位置を取得
 
        screen.blit(bg_img, (0, 0))
        screen.blit(txt.txt, (txt.x, txt.y))
        screen.blit(retry.txt, (retry.x, retry.y))
        screen.blit(quit.txt, (quit.x, quit.y))
        
        if retry.x < mouse_x < retry.x + retry.width and retry.y < mouse_y < retry.y + retry.height:
            return 0 # リトライを押された
        if quit.x < mouse_x < quit.x + quit.width and quit.y < mouse_y < quit.y + quit.height:
            return -1 # 終了を押された
        
        pg.display.update()
        clock.tick(60)


def game_clear(screen: pg.surface, clock: pg.time.Clock) -> int:
    """
    クリア画面を表示する関数
    引数: スクリーンsurface, pgのクロック
    戻り値: int(再プレイなら0, 終了なら-1)
    """
    bg_img = pg.image.load("fig/night_plain_bg.png")
    txt = Text("Game Clear", 80, (100, 300))
    retry = Text("Retry", 80, (100, 100))
    quit = Text("Quit", 80, (500, 100))

    mouse_x, mouse_y = -1000, -1000 # マウス位置をあり得ない位置で初期化

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return -1
        
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos # マウス位置を取得
 
        screen.blit(bg_img, (0, 0))
        screen.blit(txt.txt, (txt.x, txt.y))
        screen.blit(retry.txt, (retry.x, retry.y))
        screen.blit(quit.txt, (quit.x, quit.y))
        
        if retry.x < mouse_x < retry.x + retry.width and retry.y < mouse_y < retry.y + retry.height:
            return 0 # リトライを押された
        if quit.x < mouse_x < quit.x + quit.width and quit.y < mouse_y < quit.y + quit.height:
            return -1 # 終了を押された
        
        pg.display.update()
        clock.tick(60)


#ステージ構築
#---C0A24235① 追加機能
def extend(map_data: list[list[int]], add_stage_width: int, probs: list[int]) -> list[list[int]]:
    """
    ステージを拡張する関数。地面ブロックとして追加する
    内容: 下2マスは確定で地面。それ以降は拡張幅まで、下のマスが地面 and 1つ前の下のマスが地面 の時に生成
    引数: 初期マップデータ, 追加するブロックの数, 生成する確率
    戻り値: 拡張したマップのリスト
    """  
    for i in range(len(map_data)):
        layer = -1 * (i + 1)  # 下の段から選択
        if i < 2:
            for j in range(add_stage_width):  # 下2段は地面ブロック(1)
                map_data[layer].append(1)
        elif i < len(probs):
            for j in range(add_stage_width):
                pos = len(map_data[layer]) - 1  # 現時点の自身の段のブロック数-1 が自身の位置
                generate_prob = random.randint(0,100) / 100 
                if generate_prob < probs[layer] and map_data[layer + 1][pos] == 1 and map_data[layer + 1][pos + 1] == 1:
                    map_data[layer].append(1)
                else:
                    map_data[layer].append(0)
        else:
            for j in range(add_stage_width):  # 地面を生成しない段
                map_data[layer].append(0)
    return map_data


def ground_surface(map_data: list[list[int]]) -> list[list[int]]:
    """
    地面ブロックの上に地表ブロックを配置する関数
    内容: 下のマスが地面 and 自分のマスが無 の時に生成
    引数: 現在のマップデータ
    戻り値: 地表追加後のマップデータ    
    """
    for i in range(len(map_data) - 2, 0, -1): #上段から調べる
        for j in range(len(map_data[0])):  
            if map_data[i + 1][j] == 1 and map_data[i][j] == 0:
                map_data[i][j] = 2 # 地表ブロックに変更
    return map_data


def make_float_land(map_data: list[list[int]], add_range: tuple[int, int], num: int) -> list[list[int]]:
    """
    浮島を生成する関数
    内容: 自身が無の時、下のマスが無 and 2マス下が無 の時に浮島を生成
    引数: 現在のマップ, 浮島を生成するレイヤー, 生成個数 
    戻り値: 浮島を追加したマップ
    """
    maked_floatland = 0 
    while maked_floatland <= num:
        width = random.randrange(2,4) # 生成する浮島の長さ
        X = random.randrange(10, len(map_data[0])) # 浮島のX座標
        Y = random.randrange(add_range[0], add_range[1] + 1) # 浮島のY座標
        if map_data[len(map_data) - Y][X] == 0 and map_data[len(map_data) - Y + 1][X] == 0 and map_data[len(map_data) - Y + 2][X] == 0:
            maked_floatland += 1
            if X + width >= len(map_data[0]): # 生成位置がマップ範囲を超えてたらずらす
                X = len(map_data) - width
            for j in range(width):
                map_data[len(map_data) - Y][X + j] = 3
    
    for i in range(2):
        map_data[len(map_data)- 8][len(map_data[0]) - i - 1] = 3
    return map_data
#--- C0A24235① ここまで
#衝突判定
def walled(instance: object, blocks: list[pg.Rect]) -> bool: #修正
    """
    壁衝突判定を行う関数
    内容: 壁に衝突したとき、自身の位置を壁端に合わせる。
    引数: 衝突判定を行うオブジェクト, 衝突する可能性のあるブロックを保持したリスト
    戻り値: 壁にぶつかったか否かを示すbool
    """
    for block in blocks:
        if instance.rect.colliderect(block): 
            if instance.vx > 0: # 右に移動中に衝突
                instance.rect.right = block.left # 右端をブロックの左端に合わせる
                return True
            elif instance.vx < 0: # 左に移動中に衝突
                instance.rect.left = block.right # 左端をブロックの右端に合わせる
                return True


def gravity(instance: object, blocks: list[pg.Rect]) -> list[pg.Rect, int] | list[None, int]:
    """
    地面との衝突判定を行う関数
    内容: 地面にぶつかったかを判定し、ブール値で返す
    引数: 重力を適用するオブジェクト, ブロックのリスト
    戻り値: 衝突したブロックとフラグをもつリスト(1なら足元のブロック、2なら頭上ブロック)
    """

    instance.is_on_ground = False # 毎フレーム「接地していない」と仮定
    for block in blocks:
        if instance.rect.colliderect(block):
                if instance.vy > 0: # 落下中に衝突
                    return [block, 1]
                elif instance.vy < 0: # ジャンプ中に衝突
                    instance.rect.top = block.bottom # 頭をブロックの下端に合わせる
                    instance.vy = 0 # 上昇速度をリセット（頭を打った）
                    return [block, 2]
    return [None, 0]


def adjust_y(instance: object, block: pg.Rect, frag: int) -> None:
    """
    内容: instanceがブロックとy座標で衝突した際、instanceの位置を調整する
    引数: 位置調整するインスタンス, 調整位置のブロック, フラグ(1なら足元にブロック, 2なら頭上にブロック)
    """
    if frag == 1:
        instance.rect.bottom = block.top
        instance.vy = 0
        instance.is_on_ground = True
    elif frag == 2:
        instance.rect.top = block.bottom
        instance.vy = 0


def no_damage(instance: object, flag: int = 0) -> None:
    """
    無敵時間中の処理を行う関数
    内容: 無敵時間中の画像表示、無敵時間の減算
    引数: 無敵時間を適用するインスタンス, フラグ(0なら無敵時間中, 1なら無敵になる前)
    """
    if instance.no_damage_time == 0 and flag == 1:
        instance.no_damage_time = NO_DAMAGE_TIME
    elif instance.no_damage_time > 0:
        if instance.no_damage_time % 10 == 0 and instance.no_damage_time % 20 != 0:
            instance.patarn = (instance.patarn[0], 0, "normal")
        elif instance.no_damage_time % 20 == 0:
            instance.patarn = (instance.patarn[0], 0, "no_damage")            
        instance.no_damage_time -= 1
    else:
        return


def camera_adjust(instance: object, camera_x: int, stage_width: int) -> int:
    """
    instanceの位置をもとにカメラ座標を算出する関数
    引数: カメラ座標を算出するinstance, 現在のカメラ座標, ステージの広さ
    戻り値: 調整後のカメラ位置
    """
    if instance.rect.x - camera_x < LEFT_BOUND: # プレイヤーが左端
        camera_x = instance.rect.x - LEFT_BOUND # オブジェクトのずらし度を決定する。
    elif instance.rect.x - camera_x > RIGHT_BOUND: #プレイヤーが右端ならカメラの位置を右にずらす
        camera_x = instance.rect.x - RIGHT_BOUND 
    max_camera_x = stage_width * TILE_SIZE_X - SCREEN_WIDTH #カメラが右端を超えないように
    camera_x = max(0, min(camera_x, max_camera_x))
    
    return camera_x

#ーーーーーーーーーーーーークラス設定ーーーーーーーーーーーーーーーー
class Assets:
    def __init__(self):
        self.bg = pg.image.load("fig/night_plain_bg.png")
        self.ground = pg.image.load("fig/ground2.png")
        self.weeds = pg.image.load("fig/weeds(extend).png")
        self.cloud = pg.image.load("fig/cloud(extend).png")

        self.init_map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ] # 初期マップ
        self.probs = [0.5, 0.7, 0.9, 1.0, 1.0] # ブロックを生成する確率(左から上段)



class Text:
    def __init__(self, string: str, str_size: int, pos: tuple[int,int], lang: str = None) -> None:
        """
        テキストを初期化するメソッド
        内容: テキストの文字・サイズ・位置を一括設定する
        引数: 入力したい文字, 文字サイズ, 位置を示すタプル, 言語
        """
        if lang == "ja":
            self.txt = pg.font.SysFont("msgothic", str_size) # 日本語はmsゴシックで表示
        else:
            self.txt = pg.font.Font(None, str_size)
        self.txt = self.txt.render(string, True, (255, 255, 255))
        self.x = pos[0]
        self.y = pos[1]
        self.width = self.txt.get_width()
        self.height = self.txt.get_height()


class Player(pg.sprite.Sprite):
    """
    プレイヤーを司るクラス
    """
    def __init__(self):
        super().__init__()
        self.name = "normal"
        self.original = pg.image.load("fig/normal.png")
        self.img = self.original
        self.flip = pg.transform.flip(self.original, True, False)
        self.punch = pg.image.load("fig/punch.png")
        self.rect = self.img.get_rect()
        self.vx = 0
        self.vy = 0
        self.patarn = (1, 0, "normal") # プレイヤーの画像を選択する用のパターン
        self.patarn_to_img = {(1, 0, "normal") : self.img, (-1, 0, "normal") : self.flip,
                              (1, 0, "no_damage") : pg.transform.laplacian(self.img), (-1, 0, "no_damage") : pg.transform.laplacian(self.flip),
                              (1, 0, "punch") : self.punch, (-1, 0, "punch"): pg.transform.flip(self.punch, True, False)
                              }

        self.hover_num = 0
        self.hp = PLAYER_HP
        self.no_damage_time = NO_DAMAGE_TIME

        self.attacking = False # 攻撃中か
        self.is_on_ground = False # 地面についているか
        self.move_left, self.move_right = False, False


    def update(self, floar_blocks: list[pg.Rect], all_blocks: list[pg.Rect]):
        """
        自身の座標を更新する関数
        内容: キーに合わせて自身が移動する。移動に合わせてカメラ座標も取得する
        引数: 床判定ブロックリスト, 壁判定ブロックリスト       
        """ 
        if self.move_left:
            self.vx = -PLAYER_SPEED
            if self.attacking == True:
                self.patarn = (-1, 0, "punch") 
            elif self.patarn[2] == "no_damage":
                self.patarn = self.patarn
            else:
                self.patarn = (-1, 0, "normal")
        if self.move_right:
            self.vx = PLAYER_SPEED
            if self.attacking == True:
                self.patarn = (1, 0, "punch")
            elif self.patarn[2] == "no_damage":
                self.patarn = self.patarn           
            else:
                self.patarn = (1, 0, "normal")

        self.rect.x += self.vx
        walled(self, all_blocks) # 壁衝突判定

        self.vy += GRAVITY 
        self.rect.y += self.vy 
        collide = gravity(self, floar_blocks)
        if collide[1] != 0:
            self.hover_num = 0
            adjust_y(self, collide[0], collide[1])
        
        no_damage(self, 0)
    
    def hover(self) -> None:
        """
        ホバリングを行う関数
        内容: 上限まで連続して自身の上方速度を加算する。
        """
        if self.hover_num == 5:
            return
        self.vy += JUMP_STRENGTH
        self.hover_num += 1
        
    def panch(self) -> object:
        """
        パンチ攻撃を行う関数
        戻り値: 攻撃インスタンス
        """
        attack = PlayerPunch((50, 20), 600)
        self.patarn = (self.patarn[0], 0, "punch")
        self.attacking = True
        return attack

#---C0A24235② 追加機能
class Absorb(pg.sprite.Sprite):
    """吸収画像と判定を司るクラス"""
    def __init__(self):
        """
        吸収判定を初期化する関数
        引数: 吸収機能を持つインスタンス
        """
        super().__init__()
        self.original = pg.image.load("fig/absorb.png")
        self.img = self.original
        self.flip = pg.transform.flip(self.original, True, False)
        self.rect = self.img.get_rect()

    def update(self, instance: object) -> None:
        """
        吸収判定を移動させる関数
        引数: プレイヤーインスタンス
        """
        if instance.patarn[0] == 1:
            self.img = self.original
        elif instance.patarn[0] == -1:
            self.img = self.flip
        self.rect.centerx = instance.rect.centerx + instance.img.get_width() * instance.patarn[0] # 描写位置をinstanceの画像サイズと向きで再設定
        self.rect.centery = instance.rect.centery

class HoverAir(pg.sprite.Sprite):
    """ジャンプ時のエフェクト"""
    def __init__(self, instance, flag, flag_air_dire):
        super().__init__()
        self.img = pg.image.load("fig/jumped_air.png")
        self.img = [self.img, pg.transform.flip(self.img, True, False)][flag_air_dire]
        self.time = HOVER_AIR_TIME
        self.rect = self.img.get_rect()
        self.rect.x = instance.rect.centerx + instance.img.get_width() * flag
        self.rect.y = instance.rect.centery

    def update(self):
        self.time -= 1
        self.rect.y += 1
        if self.time == 0:
            self.kill()

#---C0A24235② ここまで

# ==== 追加：炎の玉 & 変身(入江) ====
class FireBall(pg.sprite.Sprite):
    """炎の玉：横に飛び、寿命で消える"""
    def __init__(self, instance: object):
        super().__init__()
        self.name = "fireball"
        self.img = pg.image.load("fig/fire.png").convert_alpha()
        self.img = pg.transform.scale(self.img, (50, 50))
        self.rect = self.img.get_rect()
        self.rect.center = instance.rect.center
        self.vx = 12 * instance.patarn[0]
        self.vy = 0
        self.gravity = 0.8
        self.damping = 0.6  # バウンドで減衰する係数
        self.life = 120  # 寿命（フレーム数) バウンドさせるため少し長めにする

    def update(self, floar_blocks: list[pg.Rect], all_blocks: list[pg.Rect]):
        # 移動（X 方向）
        self.rect.x += int(self.vx) 
        collide_x = walled(self, all_blocks) # ブロックとの水平衝突で反転（壁に当たれば跳ね返る）
        if collide_x: 
            self.vx = -self.vx * 0.6 # 水平速度を反転して減衰

        # 垂直方向の物理（重力適用）
        self.vy += self.gravity
        self.rect.y += int(self.vy)

        # ブロックとの垂直衝突（地面や天井で跳ね返す）
        collide_y = gravity(self, floar_blocks)
        if collide_y[1] != 0:
            adjust_y(self, collide_y[0], collide_y[1])
        if collide_y[1] == 1:
            self.vy = -self.vy * self.damping

        # 寿命減少
        self.life -= 1
        if self.life < 0:
            self.kill()


class BreathParticle(pg.sprite.Sprite):
    """短距離の吐息（短命・ノー重力）"""
    def __init__(self, instance: object):
        super().__init__()
        self.name = "breath"
        self.original = pg.image.load("fig/fire_beam.png")
        self.flip = pg.transform.flip(self.original, True, False)
        self.rect = self.original.get_rect()
        if instance.patarn[0] == 1:
            self.img = self.original
            self.rect.midleft = instance.rect.center
        else:
            self.img = self.flip
            self.rect.midright = instance.rect.center
        self.vx = 4 * instance.patarn[0]  # 遅くしてストリーム感を出す
        self.life = 30

    def update(self, screen: pg.Surface, camera_x: int):
        # 水平方向に移動
        self.rect.x += int(self.vx)
        self.life -= 1
        if self.life <= 0:
            self.kill()

        self.dy = random.randint(-3, 3) # 少し上下にゆらぎを入れて炎らしく見せる
        # グロー（薄い半透明の円）を先に描く
        self.glow_surf = pg.Surface((self.rect.width * 2, self.rect.height * 2), pg.SRCALPHA)
        self.glow_color = (255, 180, 70, 80)
        pg.draw.ellipse(self.glow_surf, self.glow_color, self.glow_surf.get_rect())
        screen.blit(self.glow_surf, ((self.rect.centerx - self.glow_surf.get_width() // 2) -  camera_x, self.rect.centery - self.glow_surf.get_height() // 2 + self.dy))
        screen.blit(self.img, (self.rect.x - camera_x, self.rect.y + self.dy)) # 本体を描画    


class CrashEffect(pg.sprite.Sprite):
    """自己中心の爆発エフェクト（破壊・視覚効果）"""
    def __init__(self, instance):
        super().__init__() 
        self.name = "crash"
        self.radius = 0
        self.growth = 10
        self.max_radius = 140
        self.img = pg.image.load("fig/fire_crash.png").convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.center = instance.rect.center

    def update(self):
        t =  self.radius / self.max_radius
        self.radius += self.growth 
        self.size = max(2, self.radius * 2) # スケールサイズは現在の radius に合わせる（直径）
        img = pg.transform.smoothscale(self.img, (self.size, self.size))
        alpha = int(220 * (1.0 - t)) # フェードアウトするアルファ
        img.set_alpha(alpha)
        self.img = img
        if self.size > 500:
            self.kill()


class FireAbility(Player):
    """ファイアー状態"""
    def __init__(self, instance: object):
        super().__init__()
        self.name = "fire"
        self.img = pg.image.load("fig/fire_ability2.png").convert_alpha()
        self.img = pg.transform.rotozoom(self.img, 0, 0.1)
        self.flip = pg.transform.flip(self.img, True, False)
        self.rect = instance.rect  # 既存の player_rect を共有
        self.breathing = False
        self.patarn_to_img = {(1, 0, "normal") : self.img, (-1, 0, "normal") : self.flip,
                              (1, 0, "no_damage") : pg.transform.laplacian(self.img), (-1, 0, "no_damage") : pg.transform.laplacian(self.flip),
                              (1, 0, "punch") : self.punch, (-1, 0, "punch"): pg.transform.flip(self.punch, True, False)
                              }
# ==== 追加ここまで ====


# 3.5 ボムコピー能力システムの定義
# ========================================
# 個人実装機能: ボムコピー能力 (C0C24001)
# カービィが敵を吸い込んでコピーする能力として実装
# ========================================

class BombAbility(Player):
    """ボムコピー能力クラス (C0C24001実装)
    
    カービィが爆弾を持つ敵を吸い込んだ後に使えるようになる能力
    
    使い方:
    1. 他のメンバーの吸い込みシステムから activate() を呼ぶ
    2. プレイヤーがBキーを押したら use_ability() を呼ぶ
    3. 返り値の爆弾オブジェクトを bombs リストに追加
    """
    def __init__(self, instance: object):
        super().__init__()
        self.name = "bomb"  # ボム能力を持っているか
        self.img = pg.image.load("fig/bomb_ability.png").convert_alpha()
        self.flip = pg.transform.flip(self.img, True, False)
        self.rect = instance.rect
        self.patarn_to_img = {(1, 0, "normal"): self.img, (-1, 0, "normal"): self.flip,
                              (1, 0, "no_damage"): pg.transform.laplacian(self.img), (-1, 0, "no_damage"): pg.transform.laplacian(self.flip),
                              }

    def use_ability(self, instance, ability_type="place") -> object:
        """ボム能力を使用
        
        引数:
            player_pos: プレイヤーの位置 (rect)
            player_facing_right: プレイヤーの向き
            ability_type: "place"(設置), "throw"(投擲), "kick"(キック)
            
        戻り値:
            爆弾オブジェクト または None
        """ 
        # 爆弾を生成して返す
        if ability_type == "place":
            return BombObject(instance, vx = 0, vy = 1)
        elif ability_type == "throw":
            throw_speed_x = 10 if instance.patarn[0] == 1 else -10
            throw_speed_y = -8
            return BombObject(instance, throw_speed_x, throw_speed_y)


class BombObject(pg.sprite.Sprite):
    """爆弾プロジェクタイルクラス (C0C24001実装)
    
    ボム能力で生成される爆弾オブジェクト
    
    実装機能:
    - 物理演算(重力、跳ね返り、摩擦)
    - 爆発タイマーとエフェクト
    """
    def __init__(self,instance: object, vx: int = 0, vy: int = 0):
        super().__init__()
        self.img = pg.image.load("fig/bomb.png").convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.center = instance.rect.center
        self.placed_time = time.time()  # 設置時刻
        self.is_exploded = False  # 爆発したか
        self.explosion_time = None  # 爆発時刻
        self.vx = vx  # X方向の速度
        self.vy = vy  # Y方向の速度
        self.on_ground = False  # 地面に接地しているか
        self.frame = BOMB_EXPLOSION_DURATION
         
        
    def update(self, blocks: list[pg.Rect]):
        """爆弾の状態を更新"""
        current_time = time.time()
        
        # まだ爆発していない場合、時間経過をチェック
        if not self.is_exploded:
            if current_time - self.placed_time >= BOMB_FUSE_TIME:
                self.is_exploded = True
                self.explosion_time = current_time
            
            # 重力を常に適用（地面にいない限り）
            if not self.on_ground:
                self.vy += GRAVITY * 0.5  # 爆弾用の重力（少し弱め）

            # X方向の移動
            if self.vx != 0:
                self.rect.x += self.vx
                
                # X方向の衝突チェック（壁で跳ね返る）
                collide_x = walled(self, blocks)
                if collide_x:
                    self.vx *= -self.vx * 0.5
            
            # Y方向の移動
            self.rect.y += self.vy
            collide_y = gravity(self, blocks)
            if collide_y[1] == 0:
                adjust_y(self, collide_y[0], collide_y[1])
            if collide_y[1] == 1:
                self.vy = -self.vy * 0.3  # 少し跳ねる
                self.vx *= 0.9 # 摩擦で減速
                if abs(self.vx) < 0.5:
                    self.vx = 0
                # 跳ね返りが小さい場合は停止
                if abs(self.vy * 0.3) < 1:
                    self.vy = 0
                    
    
    def draw(self, surface: pg.Surface, camera_x: int):
        """爆弾または爆発エフェクトを描画"""
        if self.is_exploded:
            explosion_center = (self.rect.centerx - camera_x, self.rect.centery)
            # 外側の円(赤)
            pg.draw.circle(surface, (255, 0, 0), explosion_center, BOMB_RADIUS, 0)
            # 中間の円(オレンジ)
            pg.draw.circle(surface, (255, 165, 0), explosion_center, BOMB_RADIUS * 2 // 3, 0)
            # 内側の円(黄色)
            pg.draw.circle(surface, (255, 255, 0), explosion_center, BOMB_RADIUS // 3, 0)

#--- 小林 追加機能
class KajinoAbility(Player):
    def __init__(self, instance: object):
        super().__init__()
        self.name = "kajino"
        self.img = pg.image.load("fig/カービィカジノ吸収.png").convert_alpha()
        self.img = pg.transform.rotozoom(self.img, 0, 0.1)
        self.flip = pg.transform.flip(self.img, True, False)
        self.rect = instance.rect
        self.patarn_to_img = {(1, 0, "normal"): self.img, (-1, 0, "normal"): self.flip,
                        (1, 0, "no_damage"): pg.transform.laplacian(self.img), (-1, 0, "no_damage"): pg.transform.laplacian(self.flip),
                        }

class KajinoBullet(pg.sprite.Sprite):
    def __init__(self, instance: object, type: int):
        super().__init__()
        self.configs = {
            1: pg.transform.rotozoom(pg.image.load("fig/きいろ.png"), 0, 0.05),      # タイプ1 (黄)
            2: pg.transform.rotozoom(pg.image.load("fig/あお.png"), 0, 0.15), # タイプ2 (青)
            3: pg.transform.rotozoom(pg.image.load("fig/あか.png"), 0, 0.2),   # タイプ3 (赤)
            99999: pg.transform.rotozoom(pg.image.load("fig/くろ.png"), 0, 0.5) ,   # 超特大 (黒)
        }
        self.name = "bullet"
        self.img = self.configs[type]
        self.rect = self.img.get_rect()
        self.rect.center = instance.rect.center
        self.vx = 15 * instance.patarn[0]
        self.time = 300

    def update(self):
        self.rect.x += int(self.vx)
        
        self.time -= 1
        if self.time <= 0:
            self.kill()

#---小林 ここまで

class Enemy(pg.sprite.Sprite):
    """敵の基本挙動・判定"""
    def __init__(self, pos: tuple[int, int]):
        super().__init__()

        self.name = "normal"
        self.original = pg.image.load("fig/troia1.png")
        self.img = self.original
        self.flip = pg.transform.flip(self.img, True, False)
        self.rect = self.img.get_rect()
        self.rect.center = pos #初期位置
        self.size = 1.0
        self.vx = -ENEMY_SPEED
        self.vy = 0
        self.patarn = (1, 0, "normal")
        self.patarn_to_img = {(1, 0, "normal"): self.img, (-1, 0, "normal"): self.flip,
                              (1, 0, "no_damage"): pg.transform.laplacian(self.img), (-1, 0, "no_damage"): pg.transform.laplacian(self.flip),
                              }

        self.hp = 5
        self.no_damage_time = NO_DAMAGE_TIME
        self.power = 1
        
        self.is_on_ground = False

    def update(self, all_blocks: list[pg.Rect], floar_blocks: list[pg.Rect]) -> None:
        """
        自身の位置を更新する関数
        引数: 壁判定用のブロックリスト, 床判定用のブロックリスト
        """
        self.rect.x += self.vx
        collide_x = walled(self, all_blocks)
        if collide_x:
            self.vx *= -1 # 壁に衝突したら反転
        
        self.vy += GRAVITY
        self.rect.y += int(self.vy)
        collide_y = gravity(self, floar_blocks)
        if collide_y[1] != 0:
            adjust_y(self, collide_y[0], collide_y[1])

#---不破　追加機能
class BombEnemy(Enemy):
    """
    爆弾の敵に関するクラス
    """
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.name = "BombEnemy"
        self.original = pg.transform.rotozoom(pg.image.load("fig/bomb_enemy.png"), 0, 1)
        self.img = self.original
        self.flip = pg.transform.flip(self.img, True, False)
        self.rect = self.img.get_rect()
        self.rect.center = pos
        self.vx = random.choice([-3, 3])
        self.vy = 0
        self.direction = int(abs(self.vx) / self.vx) # 向いている方向を設定
        self.next_throw = random.randint(60, 120) # 次に投げるタイミング
        self.patarn = (self.direction, 0, "normal")
        self.patarn_to_img = {(1, 0, "normal"): self.img, (-1, 0, "normal"): self.flip,
                              (1, 0, "no_damage"): pg.transform.laplacian(self.img), (-1, 0, "no_damage"): pg.transform.laplacian(self.flip),
                              }

    def update(self, blocks: list[pg.Rect]):
        # 横移動
        self.rect.x += int(self.vx)
        collide_x = walled(self, blocks)
        if collide_x:
            self.direction *= -1
            self.patarn = (self.direction, 0, "normal")
            self.vx *= -1

        # Y方向：重力を加算して移動
        self.vy += GRAVITY
        self.rect.y += int(self.vy)
        collide_y = gravity(self, blocks)
        if collide_y[1] != 0:
            adjust_y(self, collide_y[0], collide_y[1])


    def get_throw_velocity(self, instance: object) -> tuple[float, float]:
        """
        プレイヤー方向への投擲初速ベクトルを返す
        """
        dx = instance.rect.centerx - self.rect.centerx
        dy = instance.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            return 0.0, 0.0
        speed = 8.0
        return dx / dist * speed, dy / dist * speed


class EnemysBomb(pg.sprite.Sprite):
    """
    敵が投げたに関するクラス
    """
    def __init__(self, bomb_enemy: BombEnemy, instance: object):
        super().__init__()
        self.name = "Bomb"
        vx, vy = bomb_enemy.get_throw_velocity(instance) # 爆弾の初速ベクトル
        self.vx = vx
        self.vy = vy - 0.5
        self.img = pg.image.load("fig/bomb.png") # 画像と角度合わせ
        angle = math.degrees(math.atan2(-self.vy, self.vx))
        self.img = pg.transform.rotozoom(self.img, angle, 1)
        self.rect = self.img.get_rect()
        self.rect.center = bomb_enemy.rect.center
        self.boom_img = pg.image.load("fig/bomb_explosion2.png")
        offset = max(bomb_enemy.rect.width, bomb_enemy.rect.height) // 2 + 6 # 発射方向へのオフセット
        if not (vx == 0 and vy == 0):
            norm = math.hypot(vx, vy)
            if norm != 0:
                self.rect.centerx += int(vx / norm * offset)
                self.rect.centery += int(vy / norm * offset)

        # 爆発状態管理
        self.exploded = False
        self.boom_life = 0  # 爆発表示残フレーム数

    def update(self, blocks: list[pg.Rect]):
        if self.exploded: # 爆発中はカウントダウンして寿命が尽きたら削除
            self.boom_life -= 1
            if self.boom_life <= 0:
                self.kill()
            return

        # 少し重力を加えて落下させる
        self.vy += GRAVITY * 0.08
        # 位置更新（小数切り捨てで位置を進める）
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

        # 地面との衝突判定（衝突したら爆発表示に移行）
        for block in blocks:
            if self.rect.colliderect(block):
                # 衝突前の爆弾中心を保存（boom をここから表示する）
                old_center = self.rect.center
                # boom 画像に切り替え
                if self.boom_img:
                    self.img = pg.transform.rotozoom(self.boom_img, 0, 1)
                    self.rect = self.img.get_rect(center=old_center)
                # 移動停止して爆発状態に切替
                self.vx = 0.0
                self.vy = 0.0
                self.exploded = True
                self.boom_life = 30  # 表示フレーム（必要に応じて調整）
                break


class SlotEnemy(Enemy):
    """
    スロットの敵に関するクラス
    """
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.name = "SlotEnemy" 
        self.img = pg.transform.rotozoom(pg.image.load("fig/slot.png"), 0, 1)
        self.flip = pg.transform.flip(self.img, True, False)
        self.rect = self.img.get_rect()
        self.rect.center = pos
        self.patarn = (1, 0, "normal")
        self.patarn_to_img = {(1, 0, "normal"): self.img, (-1, 0, "normal"): self.flip,
                              (1, 0, "no_damage"): pg.transform.laplacian(self.img), (-1, 0, "no_damage"): pg.transform.laplacian(self.flip),
                              }

        self.speed = random.randrange(0, 3)  # プレイヤーの移動速度(5)より遅く
        self.vx = 0.0
        self.vy = 0.0

        self.next_shot = random.randint(60, 180) # 次弾速度
        self.weapon_speed = 8.0

    def update(self, instance: object, blocks: list[pg.Rect]):
        # プレイヤーの方向を計算
        dx = instance.rect.centerx - self.rect.centerx

        # 方向の正規化（単位ベクトル化）
        dist = abs(dx)
        if dist != 0:
            # X方向の速度を設定（正規化して speed を掛ける）
            self.vx = (dx / dist) * self.speed

        # 横移動
        self.rect.x += int(self.vx)
        walled(self, blocks)


class FireEnemy(Enemy):
    """
    炎の敵に関するクラス
    """
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.name = "FireEnemy"
        self.img = pg.transform.rotozoom(pg.image.load("fig/fire_enemy.png"), 0, 1)
        self.flip = pg.transform.flip(self.img, True, False)
        self.rect = self.img.get_rect()
        self.rect.center = pos
        self.vx = random.choice([-2, 2])
        self.vy = 0
        self.direction = int(abs(self.vx) / self.vx) # 自身の向きを設定
        self.on_ground = False
        self.next_shot = random.randint(60, 180) # 次弾の装填速度
        self.weapon_speed = 6.0 # 弾の速度
        self.patarn = (self.direction, 0, "normal")
        self.patarn_to_img = {(1, 0, "normal"): self.img, (-1, 0, "normal"): self.flip,
                              (1, 0, "no_damage"): pg.transform.laplacian(self.img), (-1, 0, "no_damage"): pg.transform.laplacian(self.flip),
                              }

    def update(self, blocks: list[pg.Rect]):
        # 横移動
        self.rect.x += int(self.vx)
        collide_x = walled(self, blocks)
        if collide_x:
            self.direction *= -1
            self.patarn = (self.direction, 0, "normal")
            self.vx *= -1

        # Y方向：重力を加算して移動
        self.vy += GRAVITY
        self.rect.y += int(self.vy)

        # Y方向の衝突チェック（プレイヤーと同じロジック）
        collide_y = gravity(self, blocks)
        if collide_y[1] != 0:
            adjust_y(self, collide_y[0], collide_y[1])
        

class SlotWeapon(pg.sprite.Sprite):
    """
    スロットから発射される弾
    """
    def __init__(self, center: tuple[int, int], vx: float, vy: float):
        super().__init__()
        angle = math.degrees(math.atan2(-vy, vx)) # 発射角度を計算
        self.name = "Slot"
        self.img = pg.transform.rotozoom(pg.image.load("fig/slot_weapon.png"), angle, 1)
        self.rect = self.img.get_rect()
        self.rect.center = center
        self.vx = float(vx) 
        self.vy = float(vy)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

class FireWeapon(pg.sprite.Sprite):
    """
    炎の敵から発射される弾
    """
    def __init__(self, sx: int, sy: int, vx: float):
        super().__init__()
        self.name = "Fire"
        self.img = pg.transform.rotozoom(pg.image.load("fig/fire_throw.png"), 0, 1)
        self.rect = self.img.get_rect()
        self.rect.center = (int(sx), int(sy))
        self.vx = float(vx)
        self.base_y = float(sy - 80) # 発射位置を調整
        self.time = 0
        
    def update(self):
        self.rect.x += int(self.vx)
        self.time += 0.1 # Y座標(振幅10ピクセルの範囲で動かす）
        self.rect.y = int(self.base_y + math.sin(self.time) * 10)
#---不破 追加機能　ここまで

class PlayerPunch(pg.sprite.Sprite):
    def __init__(self, size: tuple[int, int], time: int):
        """
        引数: 攻撃判定のサイズ
        """
        super().__init__()
        self.original = pg.Surface(size)
        self.rect = self.original.get_rect()
        self.img = self.original
        self.time = time
        self.name = "punch"
        self.dire = (1, 0) # 攻撃の向き


    def update(self, instance: object):
        if instance.move_left == True:
            self.dire = (-1, 0)
        elif instance.move_right == True:
            self.dire = (1, 0)

        if self.dire == (-1, 0):
            self.rect.x ,self.rect.y = instance.rect.left - 30, instance.rect.y + 50 # パンチ判定の位置をプレイヤーの左に
        elif self.dire == (1, 0):
            self.rect.x ,self.rect.y = instance.rect.right + 30, instance.rect.y + 50

        self.time -= 1
        if self.time == 0:
            instance.attacking = False
            instance.patarn = (instance.patarn[0], 0, "normal")
            self.kill()


class BoundBalls(pg.sprite.Sprite):
    def __init__(self, stage_width: int, tile_num_y: int):
        """
        引数: ステージx方向のブロック数, y方向に配置されるブロックの最高ブロック数        
        """
        super().__init__()
        self.img = pg.image.load("fig/virus.png")
        self.rect = self.img.get_rect()
        self.rect.center = (stage_width * TILE_SIZE_X, 0) # コースの端っこに用意
        self.vx = - 2
        self.vy = 1
        self.top_bordarline = 0 # ふわふわする上端
        self.bottom_bordarline = ((SCREEN_HEIGHT / TILE_SIZE_Y) - tile_num_y) * TILE_SIZE_Y # ふわふわする下端

    def update(self):
        self.rect.x += self.vx
        if self.vy == 1:
            self.rect.y += 3 # Y方向に動かす
            if self.rect.y >= self.bottom_bordarline:
                self.vy = -1
        elif self.vy == -1:
            self.rect.y -= 3
            if self.rect.y <= self.top_bordarline:
                self.vy = 1
        if self.rect.x <= 0:
            self.kill()


class Goal(pg.sprite.Sprite):
    def __init__(self, map_data: list[list[int]]):
        super().__init__()
        self.img = pg.image.load("fig/goal(normal).png")
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = TILE_SIZE_X * len(map_data[0]) - TILE_SIZE_X * 1.5, SCREEN_HEIGHT - TILE_SIZE_Y * 9
    

class Hp:
    def __init__(self):
        self.pic = pg.font.Font(None, 80)
        self.txt = self.pic.render("HP: ", True, (0, 0, 0))


class Heart(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pg.image.load("fig/hearts1.png")

    def update(self, instance: object, num: int):
        """
        引数: プレイヤーインスタンス, ハートの個数
        """
        if instance.hp < num:
            self.kill()


class Game_contents:
    """ゲーム開始時に初期化する変数の集合"""
    def __init__(self, map_data: list[list[int]]):
        self.enemys = pg.sprite.Group() # 敵
        self.hearts = pg.sprite.Group() # hp表示のハート
        self.hovers = pg.sprite.Group() # ジャンプ時のエフェクト
        self.bound_balls = pg.sprite.Group() # ステージギミック(上下するエネミー)
        self.absorbs = pg.sprite.Group() # 吸収
        self.bombs = pg.sprite.Group() # 味方の投げた爆弾
        self.player_attacks = pg.sprite.Group() # プレイヤーの攻撃
        self.enemy_attacks = pg.sprite.Group() # 敵の攻撃
        self.hp = Hp()
        for i in range(PLAYER_HP):
            self.hearts.add(Heart())
        self.goal = Goal(map_data)
        self.bound_balls.add(BoundBalls(len(map_data[0]), 5))  

    def add_enemys(self, type_pos: list[tuple[str, tuple[int, int]]]):
        """
        敵をマップに追加する関数
        引数: 「敵の名前と位置を保持するタプル」のリスト
        """

        for i in type_pos:
            if i[0] == "nor":
                self.enemys.add(Enemy(i[1]))
            elif i[0] == "fir":
                self.enemys.add(FireEnemy(i[1]))
            elif i[0] == "bom":
                self.enemys.add(BombEnemy(i[1]))
            elif i[0] == "slo":
                self.enemys.add(SlotEnemy(i[1]))


def main():
    # ーーーーー画面設定ーーーーー
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Go koukaton")
    clock = pg.time.Clock()
    # ーーーーーーーーーーーーーー
    respond = start_page(screen, clock) # スタート画面を表示
    if respond == -1: # 終了フラグ
        return
    
    assets = Assets() # 背景画像や初期マップデータなどを取得

    bg_img = assets.bg
    bg_width = bg_img.get_width()
    pg.mixer.music.load("fig/魔王魂(ファンタジー).mp3")
    pg.mixer.music.set_volume(0.3)
    pg.mixer.music.play(loops = -1)

    map_data = assets.init_map
    map_data = extend(map_data, ADD_STAGE_BLOCK, assets.probs) # 拡張幅に合わせてブロック生成
    map_data = ground_surface(map_data) # 地表ブロック生成
    map_data = make_float_land(map_data, (6,10), 10) # 浮島を生成

    block_rects = []
    surface_rects = []
    floatland_rects = []
    for y, row in enumerate(map_data):
        for x, tile_type in enumerate(row):
            if tile_type == 1:
                block_rects.append(pg.Rect(x * TILE_SIZE_X, y * TILE_SIZE_Y, TILE_SIZE_X, TILE_SIZE_Y))
            elif tile_type == 2:
                surface_rects.append(pg.Rect(x * TILE_SIZE_X, y * TILE_SIZE_Y + (TILE_SIZE_Y / 2), TILE_SIZE_X,TILE_SIZE_Y / 2))
            elif tile_type == 3:
                floatland_rects.append(pg.Rect(x * TILE_SIZE_X, y * TILE_SIZE_Y + (TILE_SIZE_Y / 2), TILE_SIZE_X, TILE_SIZE_Y / 2))

    floar_blocks = surface_rects + floatland_rects # 床判定用ブロック
    all_blocks = block_rects + floar_blocks # 壁判定用ブロック

    normal_enemy_num, fire_enemy_num, bomb_enemy_num, slot_enemy_num = ENEMY_NUM, 2, 2, 3 # 敵の数を決定

    normal_enemy_lst = [("nor", (random.randrange(500, len(map_data[0]) * TILE_SIZE_X), 0)) for x in range(normal_enemy_num)]
    fire_enemy_lst = [("fir", (random.randrange(500, len(map_data[0]) * TILE_SIZE_X), 0)) for x in range(fire_enemy_num)]
    bomb_enemy_lst = [("bom", (random.randrange(500, len(map_data[0]) * TILE_SIZE_X), 0)) for x in range(bomb_enemy_num)]
    slot_enemy_lst = [("slo", (random.randrange(500, len(map_data[0]) * TILE_SIZE_X), random.randrange(100, 300))) for x in range(slot_enemy_num)]

    all_enemy_lst = normal_enemy_lst + fire_enemy_lst + bomb_enemy_lst + slot_enemy_lst

    content = Game_contents(map_data)
    content.add_enemys(all_enemy_lst)
    player = Player()
    camera_x = 0
    time = 0

    #ーーーーーゲームスタートーーーーー
    while True:

        #ーーーーーゴールした時の処理ーーーーー
        if player.rect.colliderect(content.goal):
            respond = game_clear(screen, clock) # クリア画面
            if respond == -1: # 終了フラグが立ったら終了
                return
            else:
                content = Game_contents(map_data)
                content.add_enemys(all_enemy_lst)
                player = Player()
                camera_x = 0
                time = 0          
            
        if player.hp <= 0:
            respond = gameover(screen, clock) # ゲームオーバ画面を表示
            if respond == -1: # 終了フラグが立ったら終了
                return 
            else: 
                content = Game_contents(map_data)
                content.add_enemys(all_enemy_lst)
                player = Player()
                camera_x = 0
                time = 0     

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT: # 左矢印キーで移動
                    player.move_left = True

                if event.key == pg.K_RIGHT: # 右矢印キーで移動
                    player.move_right = True

                if event.key == pg.K_SPACE: # スペースボタンでジャンプ
                    player.hover()
                    if player.hover_num <= 5:
                        content.hovers.add(HoverAir(player, -1, 1))
                        content.hovers.add(HoverAir(player, 1, 0))
                        player.is_on_ground = False

                if event.key == pg.K_p: # pキーでパンチ
                    if not player.attacking:
                        content.player_attacks.add(player.panch())

                if event.key == pg.K_a: # aキーで吸収
                    content.absorbs.add(Absorb())

                if player.name == "fire": 

                    if event.key == pg.K_z: # zキーでファイアボール(ファイア状態)
                        content.player_attacks.add(FireBall(player))

                    elif event.key == pg.K_x: # xキーでファイアブレス(ファイア状態)
                        if not player.breathing:
                            player.breathing = True
                            content.player_attacks.add(BreathParticle(player))
                            player.breathing_time = 60

                    elif event.key == pg.K_c: # cキーでクラッシュ(ファイア状態)
                        content.player_attacks.add(CrashEffect(player))
                        
                # ========================================
                # 個人実装: 爆弾操作 (C0C24001)
                # ========================================
                if player.name == "bomb": # 爆弾能力を持っている場合のみ使用可能
                    if event.key == pg.K_b:
                        # Shiftキーが押されている場合は投擲、それ以外は設置
                        keys = pg.key.get_pressed()
                        if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                            new_bomb = player.use_ability(player, "throw")
                            content.bombs.add(new_bomb)
                        else:
                            # 爆弾を設置（プレイヤーの足元に設置し、重力で落下）
                            # 設置時に初期速度を設定（重力で落下させる）
                            new_bomb = player.use_ability(player, "place")
                            content.bombs.add(new_bomb)
                
                if event.key == pg.K_k:
                    # 近くの爆弾をキック
                    for bomb in content.bombs:
                        if not bomb.is_exploded and abs(bomb.vx) < 1:  # 静止している爆弾のみ
                            # プレイヤーとの距離をチェック
                            distance = ((player.rect.centerx - bomb.rect.centerx) ** 2 + 
                                       (player.rect.centery - bomb.rect.centery) ** 2) ** 0.5
                            if distance < TILE_SIZE_X * 2:  # 2タイル以内
                                # プレイヤーの向きに応じて蹴る
                                kick_speed = 8 if player.patarn[0] == 1 else -10
                                bomb.vx = kick_speed
                                bomb.vy = -3  # 少し浮かせる
                                break  # 1つだけキック

                if player.name == "kajino":
                    if event.key == pg.K_0: # 0キーで弾発射
                        if random.randrange(1, 101) <= 5: # 5%の確率で最強弾
                            type_ = 99999
                        else:
                            type_ = random.randrange(1, 4)
                        content.player_attacks.add(KajinoBullet(player, type_))

            # キーが離された時
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT: 
                    player.vx = 0
                    player.move_left = False
                if event.key == pg.K_RIGHT:
                    player.vx = 0
                    player.move_right = False
                if event.key == pg.K_a: # 吸収を解除
                    content.absorbs.empty()
                if event.key == pg.K_x: 
                    player.breathing = False

        #ーーーーーーーーーーーーーーーー
        heart_num = len(content.hearts)


        for enemy in content.enemys:
            if enemy.name == "BombEnemy": # 爆弾の敵がプレイヤーに向かって投げる1〜2秒ごとに
                if time >= enemy.next_throw and abs(player.rect.x - enemy.rect.x) < 500:
                    content.enemy_attacks.add(EnemysBomb(enemy, player))
                    enemy.next_throw = time + random.randint(60, 120)
            if enemy.name == "SlotEnemy": # SlotEnemy からの発射処理（直線、同じ速さ）
                if time >= getattr(enemy, "next_shot", 0) and abs(player.rect.x - enemy.rect.x) < 500:
                    dx = player.rect.centerx - enemy.rect.centerx # playerの方向に向かう
                    dy = player.rect.centery - enemy.rect.centery
                    dist = math.hypot(dx, dy)
                    if dist == 0:
                        vx = 0.0
                        vy = 0.0
                    else:
                        vx = dx / dist * enemy.weapon_speed
                        vy = dy / dist * enemy.weapon_speed
                    content.enemy_attacks.add(SlotWeapon(enemy.rect.center, vx, vy))
                    enemy.next_shot = time + random.randint(90, 240) # 次の発射タイミングを設定（ランダム間隔）
            if enemy.name == "FireEnemy": # 炎の敵から発射処理
                if time >= getattr(enemy, "next_shot", 0) and abs(player.rect.x - enemy.rect.x) < 500:
                    sx, sy = enemy.rect.center # 発射位置を設定（敵の中心から）
                    vx = enemy.weapon_speed # プレイヤーの方向に応じて速度の符号を決定
                    if player.rect.centerx < enemy.rect.centerx:
                        vx = -enemy.weapon_speed
                        sx = enemy.rect.left - 5 # 左向きの場合、敵の左側から発射
                    else:
                        sx = enemy.rect.right + 5  # 右向きの場合、敵の右側から発射

                    # 弾を生成してグループへ追加（Y座標はそのまま中心を使用）
                    content.enemy_attacks.add(FireWeapon(sx, sy, vx))
                    # 次の発射タイミングを設定
                    enemy.next_shot = time + random.randint(90, 240)

        # プレイヤーと敵が衝突
        for enemy in pg.sprite.spritecollide(player, content.enemys, False): 
            if player.no_damage_time == 0:
                player.hp -= 1
                for i in content.hearts:
                    i.update(player, heart_num)
                    heart_num -= 1
                no_damage(player,1) # 無敵時間をスタート

        # プレイヤーと敵の攻撃が衝突
        for attacks in pg.sprite.spritecollide(player, content.enemy_attacks, False):
            if player.no_damage_time == 0:
                player.hp -= 1
                for i in content.hearts:
                    i.update(player, heart_num)
                    heart_num -= 1
                no_damage(player,1) # 無敵時間スタート

        # 吸収判定と敵が衝突
        collisions = pg.sprite.groupcollide(content.absorbs, content.enemys, False, False)
        for absorber, hit_list in collisions.items():
            for enemy in hit_list:
                enemy.size -= 0.05 # 敵を徐々に縮小
                enemy.patarn_to_img[enemy.patarn] = pg.transform.rotozoom(enemy.patarn_to_img[enemy.patarn], 0, enemy.size) # 敵の画像を縮小後に変更
                if enemy.size <= 0.2:
                    if enemy.name == "FireEnemy":
                        player = FireAbility(player)
                    elif enemy.name == "BombEnemy":
                        player = BombAbility(player)
                    elif enemy.name == "SlotEnemy":
                        player = KajinoAbility(player)
                    enemy.kill()

        # プレイヤーの攻撃と敵が衝突
        collisions = pg.sprite.groupcollide(content.player_attacks, content.enemys, False, False)
        for attack, hit_list in collisions.items():
            for enemy in hit_list:
                if enemy.no_damage_time == 0:
                    enemy.hp -= 1
                    no_damage(enemy, 1) # 無敵時間スタート
                if enemy.hp == 0:
                    enemy.kill()

        #ステージギミックとプレイヤーが衝突
        for bound_boll in content.bound_balls:
            if player.rect.colliderect(bound_boll):
                if player.no_damage_time == 0:
                    player.hp -= 1
                    for i in content.hearts:
                        i.update(player, heart_num)
                        heart_num -= 1
                    no_damage(player,1)              

        
        camera_x = camera_adjust(player, camera_x, len(map_data[0])) # カメラ位置を調整
        
        scroll_x = -camera_x % bg_width # 背景画像の位置を調整
        screen.blit(bg_img, (scroll_x - bg_width, -100))
        screen.blit(bg_img, (scroll_x, -100))
        
        player.update(floar_blocks, all_blocks)
        screen.blit(player.patarn_to_img[player.patarn], (player.rect.x - camera_x, player.rect.y))
    
        content.hovers.update()
        for hover in content.hovers:
            screen.blit(hover.img, (hover.rect.x - camera_x, hover.rect.y))
        for i in content.absorbs:
            i.update(player)
            screen.blit(i.img, (i.rect.x - camera_x, i.rect.y))
        for bomb in content.bombs:
            bomb.update(floar_blocks)
            if bomb.is_exploded: # 爆発エフェクトが終了したら
                bomb.draw(screen, camera_x)
                bomb.frame -= 1
                if bomb.frame <= 0:
                    bomb.kill()
            else:
                screen.blit(bomb.img, (bomb.rect.x - camera_x, bomb.rect.y))

        for i in content.player_attacks:
            if i.name == "fireball":
                i.update(floar_blocks, all_blocks)
                screen.blit(i.img, (i.rect.x - camera_x, i.rect.y + TILE_SIZE_Y / 2))
            elif i.name == "breath":
                i.update(screen, camera_x)
            elif i.name == "crash":
                i.update()
                screen.blit(i.img, ((i.rect.centerx - i.size // 2) - camera_x, i.rect.center[1] - i.size // 2))
            if i.name == "bullet":
                i.update()
                screen.blit(i.img, (i.rect.x - camera_x, i.rect.y))

        for i in content.bound_balls:
            i.update()
            screen.blit(i.img, (i.rect.x - camera_x, i.rect.y))
        if time % 300 == 0: # 5秒に1体生成
            content.bound_balls.add(BoundBalls(len(map_data[0]), 5))

        for enemy in content.enemys:
            no_damage(enemy, 0)
            if enemy.name == "normal":
                enemy.update(all_blocks, floar_blocks)
                screen.blit(enemy.patarn_to_img[enemy.patarn], (enemy.rect.x - camera_x, enemy.rect.y))
            elif enemy.name == "FireEnemy":
                enemy.update(all_blocks)
                screen.blit(enemy.patarn_to_img[enemy.patarn], (enemy.rect.x - camera_x, enemy.rect.y))
            elif enemy.name == "BombEnemy":
                enemy.update(all_blocks)
                screen.blit(enemy.patarn_to_img[enemy.patarn], (enemy.rect.x - camera_x, enemy.rect.y))       
            elif enemy.name == "SlotEnemy":
                enemy.update(player, all_blocks)
                screen.blit(enemy.patarn_to_img[enemy.patarn], (enemy.rect.x - camera_x, enemy.rect.y))

        # 投げられた爆弾の更新と描画
        for attack in content.enemy_attacks:
            if attack.name == "Bomb":
                attack.update(floar_blocks)
                screen.blit(attack.img, (attack.rect.x - camera_x, attack.rect.y))
        
            # SlotEnemy の弾を更新・描画（画面外に出たら削除）
            if attack.name == "Slot":
                attack.update()
                screen.blit(attack.img, (attack.rect.x - camera_x, attack.rect.y))
                # 画面外チェックで削除
                if attack.rect.right < 0 or attack.rect.left > TILE_SIZE_X * len(map_data[0]) or attack.rect.bottom < 0 or attack.rect.top > SCREEN_HEIGHT:
                    attack.kill()

            # 炎の弾の更新と描画
            if attack.name == "Fire":
                attack.update()
                screen.blit(attack.img, (attack.rect.x - camera_x, attack.rect.y))
                # 画面外チェックで削除
                if attack.rect.right < 0 or attack.rect.left > TILE_SIZE_X * len(map_data[0]):
                    attack.kill()

        for block in block_rects:
            screen.blit(assets.ground, (block.x - camera_x, block.y, block.width, block.height))
        for block in surface_rects:
            screen.blit(assets.weeds, (block.x - camera_x,block.y))
        for block in floatland_rects:
            screen.blit(assets.cloud, (block.x - camera_x, block.y))
        screen.blit(content.goal.img, (content.goal.rect.x - camera_x, content.goal.rect.y))

        for index, i in enumerate(content.hearts, 2):
            screen.blit(i.img, (10 + (i.img.get_width() * index), 0))
        screen.blit(content.hp.txt, (0, 5))

        time += 1
        pg.display.update()
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
