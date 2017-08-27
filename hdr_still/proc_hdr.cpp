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

#define INTERACTIVE false

void printVersion() {
    cout << "Using OpenCV v"
        << CV_MAJOR_VERSION << "."
        << CV_MINOR_VERSION << "."
        << CV_SUBMINOR_VERSION << endl;
}

void procHDR(const vector<Mat>& frames, const string& newfile) {

    Mat fusion;
    Ptr<MergeMertens> merge_mertens = createMergeMertens();
    merge_mertens->process(frames, fusion);

    if (INTERACTIVE) imshow("fusion", fusion);
    imwrite(newfile, fusion * 255);
    cout << "Wrote file " << newfile << endl;
    if (INTERACTIVE) waitKey(0);
}


void loadFrames(const vector<string>& files, vector<Mat>& frames) {
    for (int i = 0; i < frames.size(); i++) {
        frames[i] = imread(files[i]);
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
    vector<Mat> frames(files.size());
    loadFrames(files, frames);


    // Create HDR image
    string str = files[0];
    int chr_idx= str.find_last_of("/");
    string newfile = str.substr(0, chr_idx) + "/hdr.jpg";
    procHDR(frames, newfile);

    return 0;
}
