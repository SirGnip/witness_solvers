'''
Run through a list of files. Serves as a type of regression test.
'''
import datetime
from dataclasses import dataclass
import runner
import cfg

FILE_AND_TYPE = (
    ('Starter2Region', 'simple1.jpg'),
    # ('Starter2Region', 'simple2.jpg'),
    # ('Starter2Region', 'simple3.jpg'),
    # ('Starter2Region', 'simple4.jpg'),
    # ('Starter2Region', 'simple5.jpg'),
    # ('Starter2Region', 'simple6.jpg'),
    # ('Starter2Region', 'simple7.jpg'),
    # ('TripletRegion', 'region2_1.jpg'),
    ('TripletRegion', 'region2_2.jpg'),
    # ('TripletRegion', 'region2_3.jpg'),
    # ('TripletRegion', 'region3_1.jpg'),
    # ('TripletRegion', 'region3_2.jpg'),
    ('TripletRegion', 'region3_3.jpg'),
    # ('Triangle', 'triangle1.jpg'),
    ('Triangle', 'triangle2.jpg'),
)

def main():
    cfg.SHOW_DEBUG_IMG = False  # hack to disable the display of debug images

    @dataclass
    class FakeArgs:
        imgpath: str
        puzzle_type: str

    for idx, (puzzle_type, name) in enumerate(FILE_AND_TYPE):
        name = 'img/' + name
        print()
        print('=' * 80, f'#{idx} of {len(FILE_AND_TYPE)}', name, puzzle_type, datetime.datetime.now())
        args = FakeArgs(name, puzzle_type)
        runner.main(args)
    print('Done', datetime.datetime.now())


if __name__ == '__main__':
    main()