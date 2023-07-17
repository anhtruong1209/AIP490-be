import gdown

url = 'https://drive.google.com/file/d/1N_guN04Kxg4cFN6qHSu5YYIp52n82zOD/view?usp=sharing'
output = 'ckpt_viton.pt'
gdown.download(url, output, quiet=False)