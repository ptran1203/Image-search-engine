from feature import (
    ImageCluster,
    ImageDescriptor,
    Database,
    BASE_DIR,
    save
)
import os

# rebuild all
if __name__ == "__main__":
    db = Database()
    cluster = ImageCluster(db.images, 32)
    #cache
    save(cluster.clustered_images(),
        os.path.join(BASE_DIR, "cache/clustered.pkl"))
    save(cluster, os.path.join(BASE_DIR, "cache/model.pkl"))