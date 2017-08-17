#include <iostream>
#include <vector>

#include "opencv2/core.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/photo/photo.hpp"

#include "opencv2/highgui/highgui.hpp"
#include "opencv2/videoio.hpp"
#include "opencv2/photo.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/opencv.hpp"

using namespace std;
using namespace cv;

void printVersion() {
    cout << "Using OpenCV v"
        << CV_MAJOR_VERSION << "."
        << CV_MINOR_VERSION << "."
        << CV_SUBMINOR_VERSION << endl;
}

int main() {
    printVersion();

    VideoCapture cap(1);

    if (!cap.isOpened()) {
        cout << "cannot open stream" << endl;
    }

    cap.set(CAP_PROP_AUTO_EXPOSURE, 0.25); // where 0.25 means "manual exposure, manual iris"
    cap.set(CV_CAP_PROP_FPS, 1);

    int count = 0;

    vector<float> times{0.0f, 0.001f, 10.0f};
    vector<Mat> frames(3);

    while (count < 3) {
        //Mat frame;
        cap.set(CAP_PROP_EXPOSURE, times[count]);

        cap.read(frames[count]);
//        cap.read(frame);
        //imshow("preview", frame);

//        if (count % flipFrames == flipFrames/2-1) {
//            cap.set(CAP_PROP_EXPOSURE, exp1);
//            cout << "exp set to " << exp1 << endl;
//        } else if (count % flipFrames == 0) {
//            cap.set(CAP_PROP_EXPOSURE, exp2);
//            cout << "exp set to " << exp2 << endl;
//        }

        cout << "exp: " << times[count] << endl;
        count++;

 //       if (waitKey(30) >= 0) {
 //           break;
 //       }
    }

    Mat response;
    Ptr<CalibrateDebevec> calibrate = createCalibrateDebevec();
    calibrate->process(frames, response, times);
    
    Mat hdr;
    Ptr<MergeDebevec> merge_debevec = createMergeDebevec();
    merge_debevec->process(frames, hdr, times, response);
    
    Mat ldr;
    Ptr<TonemapDurand> tonemap = createTonemapDurand(2.2f);
    tonemap->process(hdr, ldr);
    
    Mat fusion;
    Ptr<MergeMertens> merge_mertens = createMergeMertens();
    merge_mertens->process(frames, fusion);
    
    imwrite("fusion.png", fusion * 255);
    imwrite("ldr.png", ldr * 255);
    imwrite("hdr.hdr", hdr);

    return 0;
}
