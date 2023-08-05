from onnxmltools.convert import convert_h2o
from modelify.schema import InputList
from modelify.frameworks import BaseController
from modelify.utils import message


class H2OController(BaseController):
    def __init__(self):
        self.name = "H2O"
        super().__init__()

    def upload(self, app_uid, model, inputs:InputList, version=9):
        message("Model is converting...")
        export_path, file_name = self.export_model(model, inputs=inputs, version=version)
        message("Model converted successfully")
        super().upload_pipeline(framework_name= self.name, export_path=export_path, file_name=file_name,
         app_uid=app_uid, inputs=inputs,input_type=inputs.type)
        message("Done")


    def export_model(self, model, inputs:InputList, version):
        initial_type = inputs.convert_onnx()
        onnx = convert_h2o(model, initial_types=initial_type, target_opset=version)
        export_path, file_name = super().save_onnx_file(onnx)

        return export_path, file_name

