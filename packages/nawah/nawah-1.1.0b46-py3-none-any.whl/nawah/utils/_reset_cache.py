'''Provides `reset_cache`, `reset_expired_cache` Utility'''
import datetime
import logging

from nawah.config import Config

logger = logging.getLogger('nawah')


def reset_cache(channel: str) -> None:
    '''Resets specific cache `channel` by deleting it from active Redis db'''

    Config._sys_cache.delete(channel, '.')


def reset_expired_cache(*args, **kwargs) -> None:
    '''Deleted expired cache keys from Cache Channel'''

    logger.debug(
        'Executing `reset_expired_cache` on Cache Channels: %s', Config._cache_channels
    )

    cache = Config._sys_cache
    for channel in Config._cache_channels:
        logger.debug('Checking modules for Cache Channel: %s', channel)
        modules_keys = cache.objkeys(channel, '.')
        if not modules_keys:
            logger.debug('-Skipping Cache Channel due to no modules keys.')
            continue

        for module in modules_keys:
            logger.debug('-Checking methods for module: %s', module)
            methods_keys = cache.objkeys(channel, f'.{module}')
            if not methods_keys:
                logger.debug('--Skipping module due to no methods keys.')
                continue

            for method in methods_keys:
                logger.debug('--Checking Cache Keys for method: %s', method)
                cache_keys = cache.objkeys(channel, f'.{module}.{method}')
                if not cache_keys:
                    logger.debug('---Skipping method due to no Cache Keys.')
                    continue

                for cache_key in cache_keys:
                    logger.debug('---Checking Cache Key: %s', cache_key)
                    cache_time = cache.get(
                        channel,
                        f'.{module}.{method}.{cache_key}.results.args.cache_time',
                    )
                    cache_age = (
                        datetime.datetime.utcnow()
                        - datetime.datetime.fromisoformat(cache_time)
                    ).seconds

                    if cache_age > Config.cache_expiry:
                        logger.debug('----Cache is expired. Deleteing..')
                        cache.delete(channel, f'.{module}.{method}.{cache_key}')
                        continue

                    logger.debug('----Skipping Cache as it is still valid.')
