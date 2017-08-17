CFLAGS = `pkg-config --cflags opencv`
LIBS = `pkg-config --libs opencv`

% : %.cpp
	        g++ $(CFLAGS) $(LIBS) --std=c++11 -o $@ $< -lopencv_core -lopencv_imgproc -lopencv_objdetect -lopencv_highgui -lopencv_videoio -lopencv_features2d -lopencv_imgcodecs
