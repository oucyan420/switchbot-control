name: SwitchBot Plug Control

on:
  schedule:
    - cron: '0,30 * * * *'  # 毎時0分と30分に実行
  workflow_dispatch:  # 手動実行のトリガー

jobs:
  run-script:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install requests

    - name: Run Python script
      env:  # GitHub Secretsを環境変数として設定
        API_TOKEN: ${{ secrets.API_TOKEN }}
        SECRET_TOKEN: ${{ secrets.SECRET_TOKEN }}
        DEVICE_ID: ${{ secrets.DEVICE_ID }}
        SWITCH_STATE: ${{ secrets.SWITCH_STATE }}
      run: |
        python reizouplagmini.py

    - name: Toggle SWITCH_STATE
      if: success()  # スクリプトの実行が成功した場合のみ状態を変更
      run: |
        if [ "${{ secrets.SWITCH_STATE }}" == "OFF" ]; then
          echo "SWITCH_STATE=ON" >> $GITHUB_ENV
        else
          echo "SWITCH_STATE=OFF" >> $GITHUB_ENV
        fi
