# 编译器
CXX = g++
# 编译选项：C++17标准、关闭优化(-O0)、生成调试信息(-g)
CXXFLAGS = -std=c++17 -O0 -g
# 输出的可执行文件名
TARGET = demo
# 源文件列表
SRCS = main.cpp

# 默认目标（直接输入 make 时执行）
all: $(TARGET)

# 编译规则
$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(TARGET)

# 清理生成的文件
clean:
	rm -f $(TARGET)

# 声明伪目标，避免与同名文件冲突
.PHONY: all clean
