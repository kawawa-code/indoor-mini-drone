# 設計判断記録（ADR: Architecture Decision Record）

設計上の重要な判断を「背景・選択肢・決定・理由」の形で1件1ファイルに記録する。
後から「なぜこうしたのか」を説明できるようにするのが目的。

| No. | タイトル | 状態 |
|---|---|---|
| [0001](0001-brushed-motor.md) | 駆動方式：ブラシ付きコアレスモーター＋MOSFET直接駆動 | 決定 |
| [0002](0002-mcu-esp32-s3.md) | マイコン：ESP32-S3-WROOM-1 | 決定 |
| [0003](0003-control-web-ui.md) | 操縦：SoftAP＋WebSocket＋ブラウザUI | 決定 |
| [0004](0004-pcb-frame.md) | フレーム：PCBフレーム＋3Dプリントガード | 決定 |
| [0005](0005-imu.md) | IMU：ICM-42688-P | 提案（Phase 2でLCSC在庫を確認して確定） |
