import base64
import json
import urllib.request
import yaml
import codecs
import logging

# 提取节点
def process_urls(url_file, processor):
    try:
        with open(url_file, 'r') as file:
            urls = file.read().splitlines()

        for index, url in enumerate(urls):
            try:
                response = urllib.request.urlopen(url)
                data = response.read().decode('utf-8')
                processor(data, index)
            except Exception as e:
                logging.error(f"Error processing URL {url}: {e}")
    except Exception as e:
        logging.error(f"Error reading file {url_file}: {e}")
#提取clash节点
def process_clash(data, index):
            # 解析YAML格式的内容
            content = yaml.safe_load(data)

            # 提取proxies部分并合并到merged_proxies中
            proxies = content.get('proxies', [])
            
            for proxy in proxies:
                # 如果类型是reality
                if proxy['type'] == 'vless' :
                    server = proxy.get("server", "")
                    port = int(proxy.get("port", 443))
                    udp = proxy.get("udp", "")
                    uuid = proxy.get("uuid", "")
                    network = proxy.get("network", "")
                    tls = int(proxy.get("tls", 0))
                    xudp = proxy.get("xudp", "")
                    sni = proxy.get("servername", "")
                    flow = proxy.get("flow", "")
                    publicKey = proxy.get('reality-opts', {}).get('public-key', '')
                    short_id = proxy.get('reality-opts', {}).get('short-id', '')
                    fp = proxy.get("client-fingerprint", "")
                    insecure = int(proxy.get("skip-cert-verify", 0))
                    grpc_serviceName = proxy.get('grpc-opts', {}).get('grpc-service-name', '')

                    ws_path = proxy.get('ws-opts', {}).get('path', '')
                    ws_headers_host = proxy.get('ws-opts', {}).get('headers', {}).get('Host', '')
                    if tls == 0:
                        security = 'none'
                    elif tls == 1 and publicKey != '':
                        security = 'reality'
                    else:
                        security = 'tls'
                    vless_meta =  f"vless://{uuid}@{server}:{port}?security={security}&allowInsecure{insecure}&flow={flow}&type={network}&fp={fp}&pbk={publicKey}&sid={short_id}&sni={sni}&serviceName={grpc_serviceName}&path={ws_path}&host={ws_headers_host}#vless_meta_{index}"
                    
                    merged_proxies.append(vless_meta)
                    merged_proxies_neko.append(vless_meta)
                if proxy['type'] == 'vmess' :
                    server = proxy.get("server", "")
                    port = int(proxy.get("port", 443))
                    uuid = proxy.get("uuid", "")
                    #cipher = proxy.get("cipher", "")
                    alterId = proxy.get("alterId", "")
                    network = proxy.get("network", "")
                    tls = int(proxy.get("tls", 0))
                    if tls == 0:
                        security = "none"
                    elif tls == 1:
                        security = "tls"
                    sni = proxy.get("servername", "")
                    ws_path = proxy.get('ws-opts', {}).get('path', '')
                    ws_headers_host = proxy.get('ws-opts', {}).get('headers', {}).get('Host', '')

                    vmess_meta =  f"vmess://{uuid}@{server}:{port}?security={security}&allowInsecure{insecure}&type={network}&fp={fp}&sni={sni}&path={ws_path}&host={ws_headers_host}#vmess_meta_{index}"
                    merged_proxies.append(vmess_meta)
                    merged_proxies_neko.append(vmess_meta)
                elif proxy['type'] == 'tuic':
                    server = proxy.get("server", "")
                    port = int(proxy.get("port", 443))
                    uuid = proxy.get("uuid", "")
                    password = proxy.get("password", "")
                    sni = proxy.get("sni", "")
                    insecure = int(proxy.get("skip-cert-verify", 0))
                    udp_relay_mode = proxy.get("udp-relay-mode", "naive")
                    congestion = proxy.get("congestion-controller", "bbr")
                    alpn = proxy.get("alpn", [])[0] if proxy.get("alpn") and len(proxy["alpn"]) > 0 else None
                    tuic_meta_neko = f"tuic://{server}:{port}?uuid={uuid}&version=5&password={password}&insecure={insecure}&alpn={alpn}&mode={udp_relay_mode}"
                    tuic_meta = f"tuic://{uuid}:{password}@{server}:{port}?sni={sni}&congestion_control={congestion}&udp_relay_mode={udp_relay_mode}&alpn={alpn}&allow_insecure={insecure}"
                    merged_proxies.append(tuic_meta)
                    merged_proxies_neko.append(tuic_meta_neko)
                elif proxy['type'] == "hysteria2":
                    server = proxy.get("server", "")
                    port = int(proxy.get("port", 443))
                    auth = proxy.get("password", "")
                    obfs = proxy.get("obfs", "")
                    obfs_password = proxy.get("obfs-password","")
                    sni = proxy.get("sni", "")
                    insecure = int(proxy.get("skip-cert-verify", 0))
                    hy2_meta = f"hysteria2://{auth}@{server}:{port}?insecure={insecure}&sni={sni}&obfs={obfs}&obfs-password={obfs_password}#hysteria2_meta_{index}"
                    merged_proxies.append(hy2_meta)
                    merged_proxies_neko.append(hy2_meta)
                elif proxy['type'] == 'hysteria':
                    server = proxy.get("server", "")
                    port = int(proxy.get("port", 443))
                    ports = proxy.get("port", "")
                    protocol = proxy.get("protocol", "udp")
                    up_mbps = 50
                    down_mbps = 80                   
                    alpn = proxy.get("alpn", [])[0] if proxy.get("alpn") and len(proxy["alpn"]) > 0 else None
                    obfs = proxy.get("obfs", "")
                    insecure = int(proxy.get("skip-cert-verify", 0))
                    sni = proxy.get("sni", "")
                    fast_open = int(proxy.get("fast_open", 1))
                    auth = proxy.get("auth-str", "")
                    # 生成URL
                    hysteria_meta = f"hysteria://{server}:{port}?peer={sni}&auth={auth}&insecure={insecure}&upmbps={up_mbps}&downmbps={down_mbps}&alpn={alpn}&mport={ports}&obfs={obfs}&protocol={protocol}&fastopen={fast_open}#hysteria_meta_{index}"
                    merged_proxies.append(hysteria_meta)
                    merged_proxies_neko.append(hysteria_meta)
                elif proxy['type'] == 'ssr':
                    server = proxy.get("server", "")
                    port = int(proxy.get("port", 443))
                    password = proxy.get("password", "")
                    password = base64.b64encode(password.encode()).decode()
                    cipher = proxy.get("cipher", "")
                    obfs = proxy.get("obfs", "")
                    protocol = proxy.get("protocol", "")
                    protocol_param = proxy.get("protocol-param", "")
                    obfs_param = proxy.get("obfs-param", "")
                    # 生成URL
                    ssr_source=f"{server}:{port}:{protocol}:{cipher}:{obfs}:{password}/?remarks=ssr_meta_{index}&protoparam{protocol_param}=&obfsparam={obfs_param}"
                    
                    ssr_source=base64.b64encode(ssr_source.encode()).decode()
                    ssr_meta = f"ssr://{ssr_source}"
                    merged_proxies.append(ssr_meta)

def process_naive(data, index):
    try:
        json_data = json.loads(data)
        # 处理 shadowtls 数据

        proxy_str = json_data["proxy"]
        proxy_str = proxy_str.replace("https://", "")
        # 对 proxy 进行 Base64 编码
        encoded_proxy = base64.b64encode(proxy_str.encode()).decode()
        # 添加前缀
        naiveproxy = "http2://" + encoded_proxy
        naiveproxy_neko = f"naive+https://{proxy_str}"
        merged_proxies.append(naiveproxy)
        merged_proxies_neko.append(naiveproxy_neko)

    except Exception as e:
        logging.error(f"Error processing shadowtls data for index {index}: {e}")

def process_shadowtls(data, index):
    try:
        json_data = json.loads(data)
        # 处理 shadowtls 数据

        server = json_data["outbounds"][1]["server"]
        server_port = json_data["outbounds"][1]["server_port"]
        method = json_data["outbounds"][0]["method"]
        password = json_data["outbounds"][0]["password"]
        version = int(json_data["outbounds"][1]["version"])
        host = json_data["outbounds"][1]["tls"]["server_name"]
        ss = f"{method}:{password}@{server}:{server_port}"
        shadowtls = f'{{"version": "{version}", "host": "{host}"}}'
        shadowtls_proxy = "ss://"+base64.b64encode(ss.encode()).decode()+"?shadow-tls="+base64.b64encode(shadowtls.encode()).decode()+f"#shadowtls{index}"
        
        merged_proxies.append(shadowtls_proxy)

    except Exception as e:
        logging.error(f"Error processing shadowtls data for index {index}: {e}")
#hysteria
def process_hysteria(data, index):
    try:
        json_data = json.loads(data)
        # 处理 hysteria 数据
        # 提取字段值
        server = json_data["server"]
        protocol = json_data["protocol"]
        # up_mbps = json_data["up_mbps"]
        # down_mbps = json_data["down_mbps"]
        up_mbps = 50
        down_mbps = 100
        alpn = json_data["alpn"]
        obfs = json_data["obfs"]
        insecure = int(json_data["insecure"])
        server_name = json_data["server_name"]
        fast_open = int(json_data["fast_open"])
        auth = json_data["auth_str"]
        # 生成URL
        hysteria = f"hysteria://{server}?peer={server_name}&auth={auth}&insecure={insecure}&upmbps={up_mbps}&downmbps={down_mbps}&alpn={alpn}&obfs={obfs}&protocol={protocol}&fastopen={fast_open}#hysteria{index}"
        merged_proxies.append(hysteria)
        merged_proxies_neko.append(hysteria)

    except Exception as e:
        logging.error(f"Error processing hysteria data for index {index}: {e}")
# 处理hysteria2
def process_hysteria2(data, index):
    try:
        json_data = json.loads(data)
        # 处理 hysteria2 数据
        # 提取字段值
        server = json_data["server"]
        insecure = int(json_data["tls"]["insecure"])
        sni = json_data["tls"]["sni"]
        auth = json_data["auth"]
        # 生成URL
        hysteria2 = f"hysteria2://{auth}@{server}?insecure={insecure}&sni={sni}#hysteria2_{index}"
        merged_proxies_neko.append(hysteria2)
        merged_proxies.append(hysteria2)
    except Exception as e:
        logging.error(f"Error processing hysteria2 data for index {index}: {e}")

#处理xray
def process_xray(data, index):
    try:
        json_data = json.loads(data)
        # 处理 xray 数据
        # 提取所需字段
        protocol = json_data["outbounds"][0]["protocol"]
        server = json_data["outbounds"][0]["settings"]["vnext"][0]["address"]
        port = json_data["outbounds"][0]["settings"]["vnext"][0]["port"]
        uuid = json_data["outbounds"][0]["settings"]["vnext"][0]["users"][0]["id"]
        istls = True
        flow = json_data["outbounds"][0]["settings"]["vnext"][0]["users"][0]["flow"]
        # 传输方式
        network = json_data["outbounds"][0]["streamSettings"]["network"]
        publicKey = json_data["outbounds"][0]["streamSettings"]["realitySettings"]["publicKey"]
        shortId = json_data["outbounds"][0]["streamSettings"]["realitySettings"]["shortId"]
        serverName = json_data["outbounds"][0]["streamSettings"]["realitySettings"]["serverName"]
        fingerprint = json_data["outbounds"][0]["streamSettings"]["realitySettings"]["fingerprint"]
        spx = json_data["outbounds"][0]["streamSettings"]["realitySettings"]["spiderX"]
        # udp转发
        isudp = True
        name = f"reality{index}"
        
        # 根据network判断tcp
        if network == "tcp":
            reality = f"vless://{uuid}@{server}:{port}?security=reality&flow={flow}&type={network}&fp={fingerprint}&pbk={publicKey}&sni={serverName}&spx={spx}&sid={shortId}#REALITY{index}"

        # 根据network判断grpc
        elif network == "grpc":
            serviceName = json_data["outbounds"][0]["streamSettings"]["grpcSettings"]["serviceName"]
            reality = f"vless://{uuid}@{server}:{port}?security=reality&flow={flow}&&type={network}&fp={fingerprint}&pbk={publicKey}&sni={serverName}&spx={spx}&sid={shortId}&serviceName={serviceName}#REALITY{index}"

        # 将当前proxy字典添加到所有proxies列表中
        merged_proxies.append(reality)
        merged_proxies_neko.append(reality)
    except Exception as e:
        logging.error(f"Error processing xray data for index {index}: {e}")

def update_proxy_groups(config_data, merged_proxies):
    for group in config_data['proxy-groups']:
        if group['name'] in ['自动选择', '节点选择']:
            group['proxies'].extend(proxy['name'] for proxy in merged_proxies)

def update_warp_proxy_groups(config_warp_data, merged_proxies):
    for group in config_warp_data['proxy-groups']:
        if group['name'] in ['自动选择', '手动选择', '负载均衡']:
            group['proxies'].extend(proxy['name'] for proxy in merged_proxies)
# 定义一个空列表用于存储合并后的代理配置
merged_proxies = []
merged_proxies_neko = []
# 处理 clash URLs
process_urls('./urls/clash_new_urls.txt', process_clash)

# 处理 shadowtls URLs
process_urls('./urls/shadowtls_urls.txt', process_shadowtls)

# 处理 naive URLs
process_urls('./urls/naiverproxy_urls.txt', process_naive)

# 处理 hysteria URLs
process_urls('./urls/hysteria_urls.txt', process_hysteria)

# 处理 hysteria2 URLs
process_urls('./urls/hysteria2_urls.txt', process_hysteria2)

# 处理 xray URLs
process_urls('./urls/reality_urls.txt', process_xray)

# 将结果写入文件
try:
    with open("./sub/shadowrocket.txt", "w") as file:
        for proxy in merged_proxies:
            file.write(proxy + "\n")
except Exception as e:
    print(f"Error writing to file: {e}")
# 将结果写入文件
try:
    with open("./sub/neko.txt", "w") as file:
        for proxy in merged_proxies_neko:
            file.write(proxy + "\n")
except Exception as e:
    print(f"Error writing to file: {e}")

try:
    with open("./sub/shadowrocket.txt", "r") as file:
        content = file.read()
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    
    with open("./sub/shadowrocket_base64.txt", "w") as encoded_file:
        encoded_file.write(encoded_content)
        
    print("Content successfully encoded and written to file.")
except Exception as e:
    print(f"Error encoding file content: {e}")

try:
    with open("./sub/neko.txt", "r") as file:
        content = file.read()
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    
    with open("./sub/neko_base64.txt", "w") as encoded_file:
        encoded_file.write(encoded_content)
        
    print("Content successfully encoded and written to file.")
except Exception as e:
    print(f"Error encoding file content: {e}")