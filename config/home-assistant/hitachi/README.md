# 日立 Home Assistant 配置模板

## 文件

- `hitachi_modbus_readonly.yaml.example`：按 4 台室内机生成的只读调试模板；实际数量以寄存器 4997 为准。
- `secrets.yaml.example`：串口服务器地址和从机地址占位。

## 生成其他数量

```bash
python3 scripts/generate_hitachi_ha_yaml.py --units 4 \
  --type rtuovertcp \
  --output config/home-assistant/hitachi/hitachi_modbus_readonly.yaml
```

## 启用前

1. 从日立取得转换器型号、串口参数和从机地址。
2. 确认串口服务器工作模式：透明 RTU over TCP 时使用 `rtuovertcp`；真正 Modbus TCP 设备使用 `tcp`。
3. 先用 4998/4997 验证地址基准。
4. 完成室内机房间映射。
5. 不要自动写 4999；不要把 4004 放到普通仪表盘。

## 为什么模板暂时只读

协议把状态寄存器和控制寄存器分开，且 0.5℃ 使用独立位。先完成现场验证，再增加写脚本或 climate 封装，能避免错误控制全屋空调。
