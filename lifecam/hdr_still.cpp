#include <iostream>
#include <vector>
#include <algorithm>
#include <sstream>

#include <opencv2/photo.hpp>
#include "opencv2/imgcodecs.hpp"
#include <opencv2/highgui.hpp>

using namespace std;
using namespace cv;

void printVersion() {
    cout << "Using OpenCV v"
        << CV_MAJOR_VERSION << "."
        << CV_MINOR_VERSION << "."
        << CV_SUBMINOR_VERSION << endl;
}

void getExposureTimes(int argc, char* argv[], vector<float>& times) {
    for (int i = 1; i < argc; i++) {
        istringstream ss(argv[i]);
        float n;
        if (ss >> n) {
            times.push_back(n);
        } else {
            cerr << "Invalid number " << argv[i] << endl;
            times.clear();
            return;
        }
    }
}

int main(int argc, char* argv[]) {
    printVersion();

    // Read exposure times from input
    vector<float> times;
    getExposureTimes(argc, argv, times);

    //Defaults
    if (times.size() == 0) {
        times.push_back(0.0f);
        times.push_back(0.01f);
        times.push_back(10.0f);
    }

    cout << "Using exposure times: { ";
    for (const float& f : times) {
        cout << f << " ";
    }
    cout << "}" << endl << flush;

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
    vector<Mat> frames(times.size());
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

    imwrite("fusion.png", fusion * 255);
    imwrite("ldr.png", ldr * 255);
    imwrite("hdr.hdr", hdr);

    return 0;
}
