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


    // Exposure Times
    vector<float> times{0.0f, 0.001f, 10.0f};
    vector<Mat> frames(3);

    // Open webcam
    VideoCapture cap(1);
    if (!cap.isOpened()) {
        cout << "cannot open stream" << endl;
    }

    // Manual exposure
    cap.set(CAP_PROP_AUTO_EXPOSURE, 0.25);
    cap.set(CV_CAP_PROP_FPS, 1);

    // Grab frames
    int count = 0;
    while (count < 3) {
        cap.set(CAP_PROP_EXPOSURE, times[count]);
        cap.read(frames[count]);
        count++;
    }

    // Process HDR
    // This code will not compile bcause it requires v3.3.0
    ///////////////////////////////////////////////////////

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



    return 0;
}
