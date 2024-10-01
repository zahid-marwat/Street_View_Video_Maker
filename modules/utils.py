import cv2
import os
import math
from urllib.request import urlretrieve, urlopen


def get_sv_img(apikey_streetview, lat_lon, filename="image", savepath='PHOTO_FOLDER', picsize="640x640", heading=0, pitch=0, fov=100, verbose=False):
    base = "https://maps.googleapis.com/maps/api/streetview"
    lat_lon_str = f"{lat_lon[0]},{lat_lon[1]}"
    url = (f"{base}?size={picsize}&location={lat_lon_str}&heading={heading}&pitch={pitch}&fov={fov}&key={apikey_streetview}")

    if verbose:
        print(url)

    try:
        urlretrieve(url, os.path.join(savepath, filename + ".jpg"))
    except Exception as e:
        print(f"Error retrieving image: {e}")


def calculate_angle(point1, point2):

    # latitude and longitude in radians
    lat1, lon1 = math.radians(point1[0]), math.radians(point1[1])
    lat2, lon2 = math.radians(point2[0]), math.radians(point2[1])

    # difference in longitude
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(lat2 / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # distance between the points
    distance = 6371 * c

    # Get angle using the law of cosines
    angle = math.acos((distance**2 - 6371**2 - 6371**2) / (-2 * 6371 * 6371))

    return math.degrees(angle)

def get_video(Frames_dir,vid_path,fps):

    frame_folder = Frames_dir
    output_video = vid_path

    # Get the list of frames and sort them
    frames = [os.path.join(frame_folder, img) for img in os.listdir(frame_folder) if img.endswith('.jpg')]
    frames.sort()  # Ensure they are in the correct order

    # Read the first frame to get the width and height
    first_frame = cv2.imread(frames[0])
    height, width, layers = first_frame.shape

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For .mp4 files
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    # Write each frame to the video
    for frame in frames:
        image = cv2.imread(frame)
        video_writer.write(image)

    video_writer.release()
    cv2.destroyAllWindows()



def haversine(coord1, coord2):
    R = 3958.8  # Earth radius in miles
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c * 5280  # Convert miles to feet
    return distance

