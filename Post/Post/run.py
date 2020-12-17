from Post.app import create_app

from Post.config.db_config import LocalDBConfig
from Post.config.app_config import DevLevelAppconfig

app = create_app(LocalDBConfig, DevLevelAppconfig)
app.run(host="127.0.0.1", port=5005, debug = True)