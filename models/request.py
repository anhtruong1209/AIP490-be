import json
from fastapi import Request
from common.format_image import FormatImage
async def convert_multis_image(request: Request):
    body = await request.body()
    try:
        body = json.loads(body)
    except:
        body ={
            
        }
        pass
    form =  await request.form()
    request_form = {key: value for key,value in form.items()}
    request_query_params = {item[0]: item[1] for item in request.query_params.multi_items()}

    if "image_base64_1" in request_form: 
        image_base64_1 = request_form['image_base64_1']
    elif "image_base64_1" in request_query_params:
        image_base64_1 = request_query_params['image_base64_1']
    elif "image_base64_1" in body:
        image_base64_1 = body['image_base64_1']
    else:
        image_base64_1 = None
        
    if "image_url1" in request_form: 
        image_url1 = request_form['image_url1']
    elif "image_url1" in request_query_params:
        image_url1 = request_query_params['image_url1']
    elif "image_url1" in body:
        image_url1 = body['image_url1']
    else:
        image_url1 = None

    if "image_base64_2" in request_form: 
        image_base64_2 = request_form['image_base64_2']
    elif "image_base64_2" in request_query_params:
        image_base64_2 = request_query_params['image_base64_2']
    elif "image_base64_2" in body:
        image_base64_2 = body['image_base64_2']
    else:
        image_base64_2 = None

    if "image_url2" in request_form: 
        image_url2 = request_form['image_url2']
    elif "image_url2" in request_query_params:
        image_url2 = request_query_params['image_url2']
    elif "image_url2" in body:
        image_url2 = body['image_url2']
    else:
        image_url2 = None
        
    if "image_file1" in request_form: 
        image_file1 = request_form['image_file1']
    else:
        image_file1 = None
    if "image_file2" in request_form: 
        image_file2 = request_form['image_file2']
    else:
        image_file2 = None
    
    if "image_name1" in request_form: 
        image_name1 = request_form['image_name1']
    elif "image_name1" in request_query_params:
        image_name1 = request_query_params['image_name1']
    elif "image_name1" in body:
        image_name1 = body['image_name1']
    else:
        image_name1 = None
    
    
    if "image_name2" in request_form: 
        image_name2 = request_form['image_name2']
    elif "image_name2" in request_query_params:
        image_name2 = request_query_params['image_name2']
    elif "image_name2" in body:
        image_name2 = body['image_name2']
    else:
        image_name2 = None

    image1  =  FormatImage(image_file=image_file1,image_base64=image_base64_1,image_url=image_url1,image_name=image_name1)  
    image2  =  FormatImage(image_file=image_file2,image_base64=image_base64_2,image_url=image_url2,image_name=image_name2)
    image_read1 = image1.get_byte_file()
    image_read2 = image2.get_byte_file()
    
    return {
                "image1": image_read1, 
                "image2": image_read2, 
                "image_name1": image1.image_name,
                "image_name2": image2.image_name,
           }

async def convert_single_image(request: Request):
    body = await request.body()
    try:
        body = json.loads(body)
    except:
        body ={}
        pass
    form =  await request.form()
    request_form = {key: value for key,value in form.items()}
    request_query_params = {item[0]: item[1] for item in request.query_params.multi_items()}

    if "image_base64" in request_form: 
        image_base64 = request_form['image_base64']
    elif "image_base64" in request_query_params:
        image_base64 = request_query_params['image_base64']
    elif "image_base64" in body:
        image_base64 = body['image_base64']
    else:
        image_base64 = None
    
    if "image_url" in request_form: 
        image_url = request_form['image_url']
    elif "image_url" in request_query_params:
        image_url = request_query_params['image_url']
    elif "image_url" in body:
        image_url = body['image_url']
    else:
        image_url = None
    
    if "image_file" in request_form: 
        image_file = request_form['image_file']
    else:
        image_file = None

    

    image  =  FormatImage(image_file=image_file,image_base64=image_base64,image_url=image_url)  
    
    image_read = image.get_byte_file()
    return image_read