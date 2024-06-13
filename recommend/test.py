import numpy as np

# 參數設置
rho_res = 1          # rho的解析度
theta_res = np.pi / 180  # theta的解析度

# 計算rho的範圍
height, width = (100, 100)
max_rho = int(np.sqrt(height**2 + width**2))
accumulator = np.zeros((2 * max_rho, int(np.pi / theta_res)))

print(max_rho)