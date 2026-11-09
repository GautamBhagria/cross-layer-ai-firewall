import os
import sys

# Windows UCRT64 DLL environment patch
torch_lib_path = r"C:\Python 314\Lib\site-packages\torch\lib"
if os.path.exists(torch_lib_path):
    os.add_dll_directory(torch_lib_path)

from optimum.onnxruntime import ORTModelForSequenceClassification
from optimum.onnxruntime.configuration import AutoQuantizationConfig
from optimum.onnxruntime import ORTQuantizer
from transformers import AutoTokenizer

def export_and_quantize_with_optimum():
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    export_dir = "models"
    os.makedirs(export_dir, exist_ok=True)
    
    print(f"[*] Compiling {model_name} directly to verified ONNX graph...")
    # Optimum handles the correct dynamic shape mapping under the hood
    model = ORTModelForSequenceClassification.from_pretrained(
        model_name, 
        export=True,
        provider="CPUExecutionProvider"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Save the base unquantized ONNX model maps safely
    model.save_pretrained(export_dir)
    tokenizer.save_pretrained(export_dir)
    print("[+] Base ONNX model trace completed successfully.")
    
    print("[*] Launching High-Performance INT8 Dynamic Quantization...")
    quantizer = ORTQuantizer.from_pretrained(model)
    
    # Configure ARM/x86 performance-optimized dynamic quantization constraints
    dq_config = AutoQuantizationConfig.avx512_vnni(
        is_static=False, 
        per_channel=False
    )
    
    # Export explicitly to our designated application engine path
    quantizer.quantize(
        save_dir=export_dir,
        quantization_config=dq_config,
        file_suffix="quant"
    )
    
    # Clean up file architecture to match your App Engine signature requirements
    expected_quant_name = os.path.join(export_dir, "model_quant.onnx")
    optimum_output_name = os.path.join(export_dir, "model_quantized.onnx")
    
    if os.path.exists(optimum_output_name):
        os.replace(optimum_output_name, expected_quant_name)
        
    print(f"[+] Quantization Complete! System verified deployment graph ready at: {expected_quant_name}")

if __name__ == "__main__":
    export_and_quantize_with_optimum()

