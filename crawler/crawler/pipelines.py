# pipelines.py
import logging

from scrapy import signals
from sqlalchemy import Column, Integer, String, DateTime, UnicodeText, func
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

import json

logger = logging.getLogger(__name__)

DeclarativeBase = declarative_base()


class RawObject(DeclarativeBase):
    __tablename__ = "raw_objects"

    id = Column(Integer, primary_key=True)
    url = Column(UnicodeText)
    json = Column(UnicodeText)
    created_date = Column(DateTime, default=func.current_timestamp())
    modified_date = Column(DateTime, default=func.current_timestamp(),
                           onupdate=func.current_timestamp())

    def __repr__(self):
        return "<RawObject({})>".format(self.url)


class CrawlerPipeline(object):
    def __init__(self, settings):
        self.database = settings.get('DATABASE')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            settings=crawler.settings
        )

    def open_spider(self, spider):
        self.engine = create_engine(URL(**self.database), poolclass=NullPool, connect_args={'charset': 'utf8'})
        DeclarativeBase.metadata.create_all(self.engine, checkfirst=True)
        self.session = sessionmaker(bind=self.engine)()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        print("ITEM: ==========> {}".format(item))
        raw_object = RawObject(url=item['url'], json=json.dumps(item))
        link_exists = self.session.query(RawObject).filter_by(url=item['url']).first() is not None

        if link_exists:
            logger.info('Item {} is in db'.format(raw_object))
            return item

        try:
            self.session.add(raw_object)
            self.session.commit()
            logger.info('Item {} stored in db'.format(raw_object))
        except:
            logger.info('Failed to add {} to db'.format(raw_object))
            self.session.rollback()
            raise

        return item
