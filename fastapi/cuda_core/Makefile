NVCC = nvcc
TARGET = rainbow_app

SRC = src/main.cu src/rainbow_kernel.cu src/hash_md5.cu

all:
	$(NVCC) $(SRC) -Iinclude -o $(TARGET)

clean:
	rm -f $(TARGET)
