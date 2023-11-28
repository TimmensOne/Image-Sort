import shutil
import os
import exifread

# extracting the date, time and camera model from a file
def get_metadata(file):
    with open(file, "rb") as f:
        tags = exifread.process_file(f)
        date_time = tags.get("EXIF DateTimeOriginal")
        model = tags.get("Image Model")
        return str(date_time), str(model)

def copy_and_rename(file, source, destination):
    new_name = make_unique_name(source, file, destination)
    shutil.copy(os.path.join(source, file), os.path.join(destination, new_name))

def copy_exceptions(file, source, exception_destination):
    shutil.copy(os.path.join(source, file), os.path.join(exception_destination, file))

# create a unique name for a file
def make_unique_name(source, file, destination):
    date_time, model = get_metadata(os.path.join(source, file))
    new_name = date_time.replace(":", "-") + "_" + model + os.path.splitext(file)[1]
    if os.path.exists(os.path.join(destination, new_name)):
        index = 1
        while os.path.exists(os.path.join(destination, date_time.replace(":", "-") + "_" + model + "_" + str(index)) + os.path.splitext(file)[1]):
            index += 1
        new_name = date_time.replace(":", "-") + "_" + model + "_" + str(index) + os.path.splitext(file)[1]
    return new_name

# copy all files from one folder to another and rename them
def copy_all_files(source, destination, exception_destination):
    if not os.path.exists(destination):
        os.makedirs(destination)
    for file in os.listdir(source):
        if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mov", ".avi")):
            copy_and_rename(file, source, destination)
        else:
            # if not os.path.exists(exception_destination):
            #     os.makedirs(exception_destination)
            # copy_exceptions(file, source, exception_destination)
            print("not an image: " + file)


if __name__ == "__main__":

    exception_destination = r"C:\User\Timon\Desktop\Exceptions"
    source_directory = r"C:\Users\Timon\Desktop\Test_Images"
    destination_directory = r"C:\Users\Timon\Desktop\Images_Test"

    copy_all_files(source_directory, destination_directory, exception_destination)