from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    pic_num:list = []
    pic_tag:list = []
    pic_time:list = []
    pic_group:list = []
    pic_correct:int = 3