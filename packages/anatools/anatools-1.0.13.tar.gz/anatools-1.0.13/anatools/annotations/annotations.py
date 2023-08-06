from .convert_coco import convert_coco
from .convert_kitti import convert_kitti
from .convert_pascal import convert_pascal

class Annotations:
    """Generates annotations given a dataset directory, an output directory and mapping file.
    The dataset directory must include the Ana annotations, images and metadata folders.
    Examples of mapfiles are in the example channel at /ana/channels/example/mapfiles/.
    """

    def bounding_box_2d(self, image_path, out_dir, object_ids=None, object_types=None):
        """
        Generates images annotated with 2d bounding boxes for datasets downloaded from the Platform. Optional filter on 
        object_ids or object_types (must choose a single filter).
        
        Parameters
        ----------
        image_path : str
            Path to of specific image file to draw the boxes for.  
        out_dir : str
            File path to directory where the image should be saved to.
        object_ids : list[int]
            List of object id's to annotate. If not provided, all objects will get annotated. Choose either id or type filter.
        object_types: list[str]
            Filter for the object types to annotate. If not provided, all object types will get annotated. Choose either id or type filter.
        """
        import os
        import glob
        import json
        import numpy as np
        import cv2

        if not os.path.exists(image_path):
            print('Incorrect path to images: ' + image_path)
            return

        if object_types and object_ids:
            print('Provide either object_types OR object_ids. ')
            return

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        
        try:
            root_dir = ('/').join(image_path.split('/')[:-2])
            image_name = image_path.split('/')[-1].split('.')[0]
            image_ext = image_path.split('/')[-1].split('.')[1]

            annotation_file = root_dir+'/annotations/'+image_name+"-ana.json"
            file = open(annotation_file)
            annotations = json.load(file)
            file.close()
            
            annotation_ids = [data['id'] for data in annotations['annotations']]
            if object_ids is not None and not self.check_lists(annotation_ids, object_ids, 'object_ids'):
                return


            if object_types is not None:
                metadata_file = root_dir+'/metadata/'+image_name+'-metadata.json'
                file = open(metadata_file)
                metadata = json.load(file)
                file.close()                    

                metadata_types = list(set([data['type'] for data in metadata['objects']]))
                if not self.check_lists(metadata_types, object_types, 'object_types'):
                    return
                
                object_ids = [data['id'] for data in metadata['objects'] if data['type'] in object_types]
            
            bbox_img = cv2.imread(image_path)
            for object in annotations['annotations']:
                if object_ids is None or object['id'] in object_ids:
                    x,y,w,h = object['bbox']
                    start = (x,y)
                    end = (x+w, y+h)
                    color = [int(val) for val in np.random.randint(0, 255, 3)]
                    bbox_img = cv2.rectangle(bbox_img, start, end, color, 2)
            cv2.imwrite(out_dir+'/'+image_name+'-annotated-bbox.'+image_ext,bbox_img)
            
            print('Image saved to directory: ' + out_dir)
        except Exception as e:            
            print('Something went wrong')
            print(e)        
    
    def check_lists(self, actual, expected, name_to_check):
        """
        Helper function that checks if one list is in another for validation on bounding box annotating inputs.

        Parameters
        ----------
        actual : list
            The list of actual values found in either annotation or metadata file.
        expected : list
            The expected list that is provided from the user.
        name_to_check: str
            Name of parameter to check (either object_id or object_type).

        Returns
        -------
        bool
            True if lists are matching, False otherwise.
        """
        
        if not set(expected).issubset(set(actual)):
            out_of_bounds_check= list(set(expected) - set(actual))
            print(f'Provided {name_to_check} list has the following out of bounds: {out_of_bounds_check}. Please rerun with valid list. \nHere are all the {name_to_check} that can get annotated: ')
            print(list(set(actual)))
            return False
        return True


    def dump_coco(self, datadir, outdir, mapfile):
        """Generates annotations in the format of COCO Object Detection. See https://cocodataset.org/#format-data.
        
        Parameters
        ----------
        datadir : str
            The location of the Ana dataset.
        outdir : str
            The location to output the annotation files to.
        mapfile: str
            The location of the mapping file.
        """
        convert_coco(datadir, outdir, mapfile)

    def dump_kitti(self, datadir, outdir, mapfile):
        """Generates annotations in the format of KITTI. See https://docs.nvidia.com/metropolis/TLT/archive/tlt-20/tlt-user-guide/text/preparing_data_input.html.
        
        Parameters
        ----------
        datadir : str
            The location of the Ana dataset.
        outdir : str
            The location to output the annotation files to.
        mapfile: str
            The location of the mapping file.
        """
        convert_kitti(datadir, outdir, mapfile)

    def dump_pascal(self, datadir, outdir, mapfile):
        """Generates annotations in the format of PASCAL VOC. See https://pjreddie.com/media/files/VOC2012_doc.pdf.
        
        Parameters
        ----------
        datadir : str
            The location of the Ana dataset.
        outdir : str
            The location to output the annotation files to.
        mapfile: str
            The location of the mapping file.
        """
        convert_pascal(datadir, outdir, mapfile)
