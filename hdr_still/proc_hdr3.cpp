#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <sstream>

#include <opencv2/photo.hpp>
#include "opencv2/imgcodecs.hpp"
#include <opencv2/highgui.hpp>

using namespace std;
using namespace cv;

#define INTERACTIVE true

#define PREVIEW_WINDOW "HDR Preview"

void printVersion() {
    cout << "Using OpenCV v"
        << CV_MAJOR_VERSION << "."
        << CV_MINOR_VERSION << "."
        << CV_SUBMINOR_VERSION << endl;
}

int e1,e2,e3;
vector<Mat> frames;
string out_filename;

void procHDR(int,void*) {

    /* Exposure values @ f/3.2
     * iso100, ss1       : 11.67
     * iso100, ss300     : 12.33
     * iso200, ss2000,   : 14.33
     * iso400, ss 15000  : 16.33
     */
    //vector<float> e_times = {1.0f/3.0f, 1.0f/30.0f, 1.0f/80.0f, 1.0f/140.0f};
    vector<float> e_times = {
        //1.0f/(float)e1,
        //1.0f/(float)e2,
        //1.0f/(float)e3,
        //1.0f/(float)e4
        (float)e1*0.04f,
        (float)e2*0.04f,
        (float)e3*0.04f,
    };

    Mat response;
    Ptr<CalibrateRobertson> calibrate = createCalibrateRobertson();
    calibrate->process(frames, response, e_times);


    Mat hdr;
    //Ptr<MergeDebevec> ev_merge = createMergeDebevec();
    Ptr<MergeRobertson> ev_merge = createMergeRobertson();
    ev_merge->process(frames, hdr, e_times);

    Mat ldr;
    Ptr<TonemapDurand> tonemap = createTonemapDurand(2.2f);
    tonemap->process(hdr, ldr);

    //Mat fusion;
    //Ptr<MergeMertens> merge_mertens = createMergeMertens();
    //merge_mertens->process(images, fusion;)

    cout << "Using values: { ";
    for (float f : e_times) {
        cout << f << ", ";
    }
    cout << "}" << endl;

    //ev_merge->process(frames, fusion, e_times);

    if (INTERACTIVE) {
        //imshow(PREVIEW_WINDOW, hdr);
        imshow(PREVIEW_WINDOW, ldr);
    }
    //if (!INTERACTIVE) {
        imwrite(out_filename, ldr * 255);
        cout << "Wrote file " << out_filename << endl;
    //}
    //if (INTERACTIVE) waitKey(0);
}


void loadFrames(const vector<string>& files) {
    for (int i = 0; i < files.size(); i++) {
        frames.push_back(imread(files[i]));
    }
}

int main(int argc, char* argv[]) {
    if (INTERACTIVE) printVersion();

    vector<string> files(argv + 1, argv + argc);

    if (INTERACTIVE) {
        for (string file : files) {
            cout << file << endl;
        }
    }

    // Load images
    loadFrames(files);
    cout << "loaded " << frames.size() << " frames!" << endl;

    // Create HDR image
    string str = files[0];
    int chr_idx= str.find_last_of("/");
    out_filename = str.substr(0, chr_idx) + "/hdr_robertson.jpg";

    // Init Sliders
    e1 = 839;
    e2 = 1191;
    e3 = 0;

    // Create window
    namedWindow(PREVIEW_WINDOW, 1);

    // Create trackbars
    createTrackbar("e1", PREVIEW_WINDOW, &e1, 1200, procHDR);
    createTrackbar("e2", PREVIEW_WINDOW, &e2, 1200, procHDR);
    createTrackbar("e3", PREVIEW_WINDOW, &e3, 1200, procHDR);

    procHDR(e1, 0);

    waitKey(0);


    return 0;
}
