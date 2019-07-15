import matchzoo
from matchzoo import utils
from matchzoo.engine.base_model import BaseModel


def test_timer():
    timer = utils.Timer()
    start = timer.time
    timer.stop()
    assert timer.time
    timer.resume()
    assert timer.time > start


def test_list_recursive_subclasses():
    assert utils.list_recursive_concrete_subclasses(
        BaseModel
    )


def test_average_meter():
    am = utils.AverageMeter()
    am.update(1)
    assert am.avg == 1.0
    am.update(val=2.5, n=2)
    assert am.avg == 2.0


def test_early_stopping():
    es = utils.EarlyStopping(
        patience=1,
        key='key',
    )
    result = {'key': 1.0}
    es.update(result)
    assert es.should_stop_early is False
    es.update(result)
    assert es.should_stop_early is True
    state = es.state_dict()
    new_es = utils.EarlyStopping()
    assert new_es.should_stop_early is False
    new_es.load_state_dict(state)
    assert new_es.best_so_far == 1.0
    assert new_es.is_best_so_far is False
    assert new_es.should_stop_early is True


def test_get_file():
    _url = "https://github.com/NTMC-Community/MatchZoo-py/blob/master/LICENSE"
    file_path = utils.get_file(
        'LICENSE', _url, extract=False,
        cache_dir=matchzoo.USER_DATA_DIR,
        cache_subdir='LICENSE'
    )
    num_lines = 1819
    assert len(open(file_path, 'rb').readlines()) == num_lines
