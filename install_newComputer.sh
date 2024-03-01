# 安裝 Anaconda (請網路上看教學)
# 建立安裝到 d:\ProgramData\anaconda3 ， 因為 C 槽常常會滿，這目前 1x GB，一個 env 就 1.5 gb 左右了
# 安裝後，檢查環境變數 CONDA_PREFIX 值: d:\ProgramData\anaconda3
# 環境變數 Path 應該會有 d:\ProgramData\anaconda3\Scripts 與 d:\ProgramData\anaconda3

# 新增虛擬環境 o3d_0_18，請搭配 open3d 官網的版本事項
conda create --prefix d:\ProgramData\anaconda3\envs\o3d_0_18 python=3.10

# 在 o3d_0_18 環境中安裝 open3d, linque
activate o3d_0_18
pip install open3d
pip install linque