import pygame
import os
import random

# 1. 定数と初期設定
# pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LEFT_BOUND = SCREEN_WIDTH // 3
RIGHT_BOUND = SCREEN_WIDTH * 2 // 3
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ADD_STAGE_BLOCK = 100
TILE_SIZE = 40
GRAVITY = 0.8         # 重力
JUMP_STRENGTH = -15   # ジャンプ力 (Y軸は上がマイナス)
PLAYER_SPEED = 5      # 左右の移動速度

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)   # プレイヤーの色
BROWN = (139, 69, 19)   # ブロックの色

# 画面設定
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2Dアクションゲーム デモ")
clock = pygame.time.Clock()

# 2. ステージデータ (0=空, 1=ブロック)
# 画面下部が地面、途中に浮島があるマップ
map_data = [
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def Extend(map_data, stage_width):
    """
    ステージを拡張する関数
    引数: 追加するブロックの数
    """
    for h in range(stage_width):
        for i in range(len(map_data)):
            if i < len(map_data) - 3:
                map_data[i].append(0)
            else:
                map_data[i].append(1)
    return map_data
# 3. ステージの「当たり判定用の四角形(Rect)」リストを作成
# (ゲーム開始時に一度だけ計算する)
map_data = Extend(map_data, ADD_STAGE_BLOCK)
block_rects = []
edge_rects = []
for y, row in enumerate(map_data):
    for x, tile_type in enumerate(row):
        if tile_type == 1:
            # (x座標, y座標, 幅, 高さ) のRectを作成
            block_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        elif tile_type ==2:
            edge_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
# 4. プレイヤー設定
# プレイヤーを (幅20, 高さ40) の四角形として定義
# player_img = pygame.image.load("fig/protagonist.png")
# player_img_rect = pygame.rect()
player_rect = pygame.Rect(100, 100, TILE_SIZE // 2, TILE_SIZE) 
player_velocity_y = 0  # プレイヤーの垂直方向の速度
is_on_ground = False     # 地面（ブロック）に接地しているか
player_move_left = False # 左に移動中か
player_move_right = False# 右に移動中か

camera_x = 0

# 5. ゲームループ
running = True
while running:
    
    # 6. イベント処理 (キー操作など)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # キーが押された時
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_move_left = True
            if event.key == pygame.K_RIGHT:
                player_move_right = True
            if event.key == pygame.K_SPACE and is_on_ground:
                player_velocity_y = JUMP_STRENGTH # 上向きの速度を与える
                is_on_ground = False
        
        # キーが離された時
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_move_left = False
            if event.key == pygame.K_RIGHT:
                player_move_right = False

    # 7. プレイヤーのロジック更新 (移動と当たり判定)
    
    # --- 左右の移動と当たり判定 ---
    player_movement_x = 0
    if player_move_left:
        player_movement_x -= PLAYER_SPEED
    if player_move_right:
        player_movement_x += PLAYER_SPEED
    
    player_rect.x += player_movement_x # まずX方向に動かす
    player_screen_x = player_rect.x - camera_x
    if player_screen_x < LEFT_BOUND:
        camera_x = player_rect.x - LEFT_BOUND
    elif player_screen_x > RIGHT_BOUND:
        camera_x = player_rect.x - RIGHT_BOUND
    max_camera_x = len(map_data[0]) * TILE_SIZE - SCREEN_WIDTH
    camera_x = max(0, min(camera_x, max_camera_x))
    
    # X方向の衝突チェック
    for block in block_rects:
        if player_rect.colliderect(block):
            if player_movement_x > 0: # 右に移動中に衝突
                player_rect.right = block.left # 右端をブロックの左端に合わせる
            elif player_movement_x < 0: # 左に移動中に衝突
                player_rect.left = block.right # 左端をブロックの右端に合わせる

    # --- 垂直方向（重力・ジャンプ）の移動と当たり判定 ---
    player_velocity_y += GRAVITY # 重力を速度に加算
    player_rect.y += player_velocity_y # Y方向に動かす
    
    # Y方向の衝突チェック
    is_on_ground = False # 毎フレーム「接地していない」と仮定
    for block in block_rects:
        if player_rect.colliderect(block):
            if player_velocity_y > 0: # 落下中に衝突
                player_rect.bottom = block.top # 足元をブロックの上端に合わせる
                player_velocity_y = 0 # 落下速度をリセット
                is_on_ground = True   # 接地フラグを立てる
            elif player_velocity_y < 0: # ジャンプ中に衝突
                player_rect.top = block.bottom # 頭をブロックの下端に合わせる
                player_velocity_y = 0 # 上昇速度をリセット（頭を打った）
        # if player_rect.colliderect(edge):
            # player_rect.left = edge.right

    # 8. 描画処理
    screen.fill(BLACK) # 画面を黒で塗りつぶし
    

    # ステージ（ブロック）を描画
    for block in block_rects:
        draw_rect = pygame.Rect(
            block.x - camera_x,
            block.y,
            block.width,
            block.height
        )
        pygame.draw.rect(screen, BROWN, draw_rect)
    for edge in edge_rects:
        pygame.draw.rect(screen, BLACK, edge)
        
    # プレイヤーを描画
    pygame.draw.rect(screen, GREEN, pygame.Rect(player_rect.x - camera_x, player_rect.y, player_rect.width, player_rect.height))
    
    # 画面を更新
    pygame.display.flip()
    
    # 9. FPS (フレームレート) の制御
    clock.tick(60) # 1秒間に60回ループが回るように調整

# ループが終了したらPygameを終了
pygame.quit()