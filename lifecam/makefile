# What I was using previously
# CFLAGS = `pkg-config --cflags opencv`
# LIBS = `pkg-config --libs opencv`

# This still uses 3.2
CFLAGS = -I/usr/local/include/opencv2 -I/usr/local/include

# This also still uses 3.2
# CFLAGS = -I/home/ltumcs/opencv3/opencv-3.3.0/include
LIBS = -L/usr/lib -lopencv_core -lopencv_imgproc -lopencv_objdetect -lopencv_highgui -lopencv_videoio -lopencv_features2d -lopencv_imgcodecs -lopencv_photo

% : %.cpp
	g++ $(CFLAGS) --std=c++11 -o $@ $< $(LIBS)
