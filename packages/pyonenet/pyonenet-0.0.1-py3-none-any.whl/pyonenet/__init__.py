import requests
import json


def upload_datapoint(onenet_triad, data_list):
    '''
    onenet上传数据点API
   入参：
       onenet_triad(dic)：onenet信息三元组，格式为：
           {
               product_id(str): "产品ID",
               device_id(str): "设备ID",
               api_key(str)："设备的APIKey或者masterKey"
           }
       data_list(list)：上述数据点列表，格式为：
           [
               {
               id(str): "数据点的ID",
               data(string/int/json): 上传的数据,
               at(date 选填)：为空获取当前时间，若存在，格式必须为"YYYY-MM-DDThh:mm:ss"的形式（例如：2015-03-22T22:31:12）
               },
               ...
           ]

    出参：
        response(dic): onenet返回信息，格式为：
            {
                'errno'(int): 0,
                'error'(str): 'successful'
            }
   '''

    # 构建请求头
    headers = {
        'api-key': onenet_triad.get('api_key')
    }
    body = {}

    body["datastreams"] = [
        {
            "id": data_list[i].get('id'),
            "datapoints": [
                {
                    "value": data_list[i].get('data'),
                    "at": data_list[i].get('at')
                }
            ]
        }
        for i in range(len(data_list))
    ]

    # 构造URL
    url = 'http://api.heclouds.com/devices/%s/datapoints' % onenet_triad.get(
        'device_id')
    # 发送request请求，增加数据点
    response = requests.post(url, headers=headers, data=json.dumps(body)).text
    response = json.loads(response)
    return response


def query_datastream(onenet_triad, datastream_id):
    '''
    onenet单个数据流查询API
   入参：
       onenet_triad(dic)：onenet信息三元组，格式为：
           {
               product_id(str): "产品ID",
               device_id(str): "设备ID",
               api_key(str)："设备的APIKey或者masterKey"
           }
       datastream_id(str)："数据流ID"

    出参：
        response(dic): onenet返回信息，格式为：
            {
                'errno'(int): 调用错误码，为0表示调用成功
                'error'(str): 错误描述，为"succ"表示调用成功
                'data'(json): 接口调用成功之后返回的设备相关信息，见data描述
            }
    data描述表：
        id(str): 数据流ID
        create_time(str): 数据流创建时间
        update_at(str): 最新数据上传时间
        current_value(string/int/json): 最新数据点
   '''

    # 构建请求头
    headers = {
        'api-key': onenet_triad.get('api_key')
    }

    # 构造URL
    url = 'http://api.heclouds.com/devices/%s/datastreams/%s' % (
        onenet_triad.get('device_id'), datastream_id)
    # 发送request请求，增加数据点
    response = requests.get(url, headers=headers).text
    response = json.loads(response)
    return response


def main():
    pass


def test():
    onenet_triad = {
        'product_id': "487189",
        'device_id': "890412456",
        'api_key': "vIXQrguZ4RizQS3sHSYD8njMGss="
    }
    response = query_datastream(onenet_triad, 'ch02')
    print(response)


if __name__ == '__main__':
    test()
else:
    main()
