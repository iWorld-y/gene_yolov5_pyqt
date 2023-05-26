import argparse
import logging

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='weights/yolov5s.pt', help='model.pt path(s)')
    parser.add_argument('--file', type=str, default='weights/yolov5s.pt', help='model.pt path(s)')
    args = parser.parse_args()
    logging.info(type(args))
    logging.info(args)
    logging.info(type(args.weights))
    logging.info(args.weights)
