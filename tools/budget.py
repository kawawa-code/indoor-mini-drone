"""重量・推力・電力・寸法バジェット計算。

値はすべて設計初期の見積もり（推定値）。部品が届いたら実測値で上書きし、
再計算して docs/02_system_architecture.md の表を更新する。

使い方:
    python tools/budget.py
"""

import math

# ---------------------------------------------------------------------------
# 重量 [g]  (名称, 1個あたり, 個数, 根拠)
# ---------------------------------------------------------------------------
WEIGHTS = [
    ("PCBフレーム (FR4 1.0mm)",       6.0, 1, "面積から概算"),
    ("ESP32-S3-WROOM-1",               3.5, 1, "データシート寸法から概算"),
    ("IMU・MOSFET・受動部品",          1.0, 1, "概算"),
    ("モーター 8520 コアレス",         5.0, 4, "販売ページ値、要実測"),
    ("プロペラ 55mm",                  0.5, 4, "販売ページ値、要実測"),
    ("LiPo 1S 500mAh",                12.0, 1, "販売ページ値、要実測"),
    ("プロペラガード (PLA)",           1.5, 4, "CAD体積×密度で後日更新"),
    ("配線・コネクタ・バッテリー固定", 2.0, 1, "概算"),
]

# ---------------------------------------------------------------------------
# 推進系・電源
# ---------------------------------------------------------------------------
MOTOR_COUNT = 4
THRUST_MAX_PER_MOTOR_G = 30.0   # 8520 + 55mm, 1S フルスロットル（要推力試験）
CURRENT_MAX_PER_MOTOR_A = 2.5   # フルスロットル時（要実測）
HOVER_EFFICIENCY_G_PER_W = 3.5  # ホバリング時の推力効率（小径コアレスの一般的な値）
ELECTRONICS_CURRENT_A = 0.15    # ESP32 Wi-Fi 動作時の平均（ピークは約0.5A）

BATTERY_CAPACITY_MAH = 500
BATTERY_NOMINAL_V = 3.7
BATTERY_USABLE_RATIO = 0.8      # 過放電を避けるため 80% までしか使わない
BATTERY_C_RATING = 25

# ---------------------------------------------------------------------------
# 寸法 [mm]
# ---------------------------------------------------------------------------
MOTOR_DIAGONAL_MM = 100.0       # 対角モーター軸間距離
PROP_DIAMETER_MM = 55.0
GUARD_GAP_MM = 2.5              # プロペラ先端とガード内壁の隙間
GUARD_WALL_MM = 1.2

# ---------------------------------------------------------------------------
# 要求値（docs/01_requirements.md と対応）
# ---------------------------------------------------------------------------
REQ_MAX_WEIGHT_G = 60.0         # REQ-P01
REQ_MIN_TW_RATIO = 2.0          # REQ-P02
REQ_MIN_FLIGHT_MIN = 4.0        # REQ-P03
REQ_MAX_OUTLINE_MM = 150.0      # REQ-M02


def check(ok: bool) -> str:
    return "OK" if ok else "NG"


def main() -> None:
    print("## 重量バジェット\n")
    print("| 項目 | 単重 [g] | 個数 | 小計 [g] | 根拠 |")
    print("|---|---:|---:|---:|---|")
    total = 0.0
    for name, w, n, note in WEIGHTS:
        total += w * n
        print(f"| {name} | {w:.1f} | {n} | {w * n:.1f} | {note} |")
    print(f"| **合計** | | | **{total:.1f}** | |\n")

    thrust_max = THRUST_MAX_PER_MOTOR_G * MOTOR_COUNT
    tw_ratio = thrust_max / total
    hover_throttle = total / thrust_max  # 推力∝スロットルの粗い近似

    hover_power_w = total / HOVER_EFFICIENCY_G_PER_W
    hover_current_a = hover_power_w / BATTERY_NOMINAL_V + ELECTRONICS_CURRENT_A
    usable_mah = BATTERY_CAPACITY_MAH * BATTERY_USABLE_RATIO
    flight_min = usable_mah / 1000 / hover_current_a * 60

    peak_current_a = CURRENT_MAX_PER_MOTOR_A * MOTOR_COUNT + 0.5
    battery_max_a = BATTERY_CAPACITY_MAH / 1000 * BATTERY_C_RATING

    adjacent_mm = MOTOR_DIAGONAL_MM / math.sqrt(2)
    guard_od_mm = PROP_DIAMETER_MM + 2 * (GUARD_GAP_MM + GUARD_WALL_MM)
    guard_clearance_mm = adjacent_mm - guard_od_mm
    outline_mm = adjacent_mm + guard_od_mm

    print("## 推力・電力・寸法\n")
    print("| 項目 | 値 | 要求 | 判定 |")
    print("|---|---:|---:|:---:|")
    print(f"| 総重量 | {total:.1f} g | ≤ {REQ_MAX_WEIGHT_G:.0f} g | {check(total <= REQ_MAX_WEIGHT_G)} |")
    print(f"| 最大推力 | {thrust_max:.0f} g | - | - |")
    print(f"| 推力重量比 | {tw_ratio:.2f} | ≥ {REQ_MIN_TW_RATIO:.1f} | {check(tw_ratio >= REQ_MIN_TW_RATIO)} |")
    print(f"| ホバリングスロットル（概算） | {hover_throttle * 100:.0f} % | - | - |")
    print(f"| ホバリング電流 | {hover_current_a:.2f} A | - | - |")
    print(f"| 飛行時間 | {flight_min:.1f} 分 | ≥ {REQ_MIN_FLIGHT_MIN:.0f} 分 | {check(flight_min >= REQ_MIN_FLIGHT_MIN)} |")
    print(f"| ピーク電流 | {peak_current_a:.1f} A | ≤ 電池許容 {battery_max_a:.1f} A | {check(peak_current_a <= battery_max_a)} |")
    print(f"| 隣接モーター間距離 | {adjacent_mm:.1f} mm | - | - |")
    print(f"| ガード外径 | {guard_od_mm:.1f} mm | - | - |")
    print(f"| ガード同士の隙間 | {guard_clearance_mm:.1f} mm | > 0 mm | {check(guard_clearance_mm > 0)} |")
    print(f"| 外形（ガード込み） | {outline_mm:.1f} mm 角 | ≤ {REQ_MAX_OUTLINE_MM:.0f} mm | {check(outline_mm <= REQ_MAX_OUTLINE_MM)} |")


if __name__ == "__main__":
    main()
