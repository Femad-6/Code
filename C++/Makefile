# Makefile for EMG Robotic Arm System

CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2
LDFLAGS = -pthread

# Target executable
TARGET = emg_robotic_arm
SOURCE = emg_robotic_arm.cpp

# Default target
all: $(TARGET)

# Build the main executable
$(TARGET): $(SOURCE)
	$(CXX) $(CXXFLAGS) $(SOURCE) -o $(TARGET) $(LDFLAGS)

# Clean build artifacts
clean:
	rm -f $(TARGET) *.o

# Run the program
run: $(TARGET)
	./$(TARGET)

# Debug build
debug: CXXFLAGS += -g -DDEBUG
debug: $(TARGET)

# Install dependencies (if needed)
install-deps:
	@echo "No additional dependencies required for this project"

# Help target
help:
	@echo "Available targets:"
	@echo "  all       - Build the EMG robotic arm executable (default)"
	@echo "  clean     - Remove build artifacts"
	@echo "  run       - Build and run the program"
	@echo "  debug     - Build with debug information"
	@echo "  help      - Show this help message"

.PHONY: all clean run debug install-deps help