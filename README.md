# MIS-Assessment
As the trained model was too big to be uploaded on GitHub, please download it from the following link: https://drive.google.com/file/d/1EOalcTvJvNmeY0mRIcId8bUjnMSt3Dc9/view?usp=drive_link and place the downloaded file into the cloned repository. Then, create the virtual Conda environment by running the following command inside the cloned directory:

```conda env create -f environment.yml```

Afterwards, run the main.py file by passing the path to the images folder into the main function. I am attaching a folder called "test_data", which contains the 6 images given in the original assessment repository, and by default those are the inputs into the main function. 

NOTE: The YOLO model was trained on Google Colab, and 'best.pt' is the best version downloaded after training. 'data_proccess.ipynb' contains functions that are not used in the main function, but were used during my project. The training data was too big to upload, so please find the link to download it here: https://drive.google.com/drive/folders/1uSiCzFPNQQfy6bryHNayL8Tr-VFhbU1U?usp=sharing

UPDATE: I have uploaded the model outputs for 2 cases: first 6 images have been passed into the model directly, while the remaining 12 images represent the same 6 images from the first case but have now been split in half before being passed into the model. These images can later be merged back together if necessary. 

Thank you for your consideration!
