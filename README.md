# indoor-mini-drone

屋内で飛ばす小型クアッドコプターを、**基板設計・筐体設計・ファームウェアまですべて自作する**プロジェクトです。
姿勢推定とカスケードPIDによる姿勢制御を、実装を通して学ぶことを目的としています。

> 状態：**Phase 0（要求定義）**

## 仕様（目標）

| 項目 | 値 |
|---|---|
| 総重量 | 60g以下（見積もり52.5g） |
| サイズ | 対角100mm、ガード込みで約133mm角 |
| 電源 | 1S LiPo 500mAh |
| モーター | 8520 ブラシ付きコアレス ×4、55mmプロペラ |
| マイコン | ESP32-S3-WROOM-1 |
| IMU | ICM-42688-P |
| 操縦 | Androidスマホのブラウザ（Wi-Fi / WebSocket） |
| 飛行モード | 角度モード（セルフレベル） |
| 飛行時間 | 4分以上（見積もり5.7分） |

## ドキュメント

- [01 要求仕様書](docs/01_requirements.md)
- [02 システム構成・バジェット](docs/02_system_architecture.md)
- [03 Phase 1 購入リスト](docs/03_phase1_shopping_list.md)
- [設計判断記録（ADR）](docs/adr/README.md)

## ロードマップ

- [x] Phase 0：要求定義・システム構成・バジェット
- [ ] Phase 1：ブレッドボード試作（推力試験・IMU・通信）
- [ ] Phase 2：回路設計（KiCad）・デザインレビュー
- [ ] Phase 3：基板レイアウト・JLCPCBへ発注
- [ ] Phase 4：筐体設計（Fusion 360）・3Dプリント
- [ ] Phase 5：基板の立ち上げ試験（bring-up）
- [ ] Phase 6：ファームウェア（姿勢推定・PID・フェイルセーフ）
- [ ] Phase 7：PIDチューニング・飛行評価
- [ ] Phase 8：まとめ

## フォルダ構成

```
docs/         要求仕様・設計資料・ADR・試験記録
hardware/     KiCadプロジェクト・製造データ
mechanical/   Fusion 360からのエクスポート（STEP/STL）
firmware/     Arduinoスケッチ
tools/        計算・ログ解析用のPythonスクリプト
```

## 開発環境

- KiCad 9 / Fusion 360 / Arduino IDE 2（arduino-esp32）/ Python 3.11

## ライセンス

[MIT](LICENSE)
