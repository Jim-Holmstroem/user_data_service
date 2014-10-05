#!/usr/bin/env python
from __future__ import print_function

from user_data_service.service import Service


if __name__ == '__main__':
    service = Service()
    service.run(debug=False)
