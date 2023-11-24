**Repository Description:**

Title: **Flask Image Editor with OpenCV**

This repository contains a Flask-based web application that utilizes the OpenCV library to perform various image editing operations. The application provides functionalities to upload, edit, and download images. It includes features such as flipping images vertically and horizontally, applying sharpening effects, blurring images, converting images to black and white, and removing backgrounds using an external API.

**Key Features:**

1. **Image Uploading:** Users can upload images through the web interface, which are then stored in a designated folder.

2. **Editing Options:** Users can choose from a variety of image editing options, including flipping the image vertically or horizontally, sharpening, blurring, converting to black and white, and removing backgrounds.

3. **Image Manipulation:** Each selected editing option produces a modified version of the uploaded image. These edited images are stored and can be downloaded individually.

4. **Database Integration:** The application utilizes SQLAlchemy to interact with a database, storing information about uploaded images and their edited versions.

5. **Download Capability:** Users have the ability to download both the original and edited versions of the images.

6. **API Integration:** The application integrates an external API (`remove.bg`) to facilitate the removal of image backgrounds, enhancing image editing capabilities.

**Usage:**

To use the application, run the Flask server locally, navigate to the provided URL, and interact with the user interface to upload, edit, and download images.

**Dependencies:**

- Flask
- Flask-SQLAlchemy
- OpenCV (cv2)
- Requests
- Python-dotenv
- Werkzeug

**Getting Started:**

1. Clone the repository.
2. Install the necessary dependencies.
3. Set up environment variables using a `.env` file (for database URI and secret key).
4. Run the Flask application and access it via a web browser.

**Note:** Ensure that the necessary Python packages are installed and properly configured before running the application.

This repository serves as a versatile image editing tool powered by Flask and OpenCV, offering a simple yet comprehensive solution for image manipulation via a web interface.
