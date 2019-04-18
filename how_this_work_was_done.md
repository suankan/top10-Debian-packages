# Description

This doco describes how I was doing this project.

- I've got an email with the task assignment somewhere in the evening of Tue 16 Apr but I couldn't get started straight away.
- Started looking at this task early in the morning on 18 Apr Thu.
- I sketched all my thoughts straight away into the [readme.md as a draft](https://github.com/suankan/package_statistics/tree/3fc8465d68beb8db5750fe80a25c2fdc264213dd).
- Then I straight away manually downloaded file Contents-amd64.gz, ungzipped it and [mocked up the main algorithm](https://github.com/suankan/package_statistics/tree/0ffcad87196042e5c1ae0d1489a11dc1261b02b5) of finding the biggest package.
- Then I went to my day job :)
- Then I took some time during the mid-day and briefly mocked up a [structure for a `contents_index` class](https://github.com/suankan/package_statistics/blob/5128a83dd5b60da1a42843fe0f27c0fa6d1c9882/contents_index.py). Briefly, but with enough documentation in order to not get lost my thoughts :)
- A bit later I got back to this project again and tried think what should be a good way to process each line in Contents-amd64.gz. Looked into the file again, read to Debian doc again. Finaly decided to [write up a function](https://github.com/suankan/package_statistics/blob/018648d24a555a9e1c05e23e45870b5ecbc16372/contents_index.py#L35-L89) that will handle comma-separated list of packages in a single line like 'filename    pkg1,pkg2,...,pkgN'. Also added couple of unit tests to it to make sure it works as expected.
- Later after work, I came back again to this. I decided I need to implement downloading of the file and ungzipping. And so [I've done that](https://github.com/suankan/package_statistics/commit/718531975fbfd68acfd20a17a7a9b134fe753911). Along that way I've learned something interesting about downloading binary data via `requests.get` and espessially using flag `stream=True` and reading data in chunks.
- Then I started trying to read gzipped file which I downloaded on the previous step and applying the [initial alrorithm](https://github.com/suankan/package_statistics/blob/master/readme.md#first-thoughts-on-algorithm) to it.
- And I hit a BUG as a result :) I described the issue [here](https://github.com/suankan/package_statistics/issues/1) as well as how to fix it.
- Then I took some time to fix the bug. The fix was pretty simple so I've applied it. To make sure this bug will be visible I added special unit test for that particular use case.
- After that I've finished writing [`get_packages_size()` function which does all calculations](https://github.com/suankan/package_statistics/blob/80759411d418735219972fc9996458139a55ed05/contents_index.py#L122-L151) and [wrote a unit test for it](https://github.com/suankan/package_statistics/blob/80759411d418735219972fc9996458139a55ed05/contents_index_tests.py#L65-L84) as well.
- As a next step I've coded how to actually [get top N biggest packages](https://github.com/suankan/package_statistics/blob/387d20f3df813cdc82d892661a0cb12210f27df9/contents_index.py#L155-L161) out of our calculated sizes of all packages. That was rather simple as I just re-used a ready function heapq.nlargest() which does exactly what we need.
- As a last step I've created a separate cmd `package_statistics.py` which simply imports our class and calls needed methods.
- And finally I took a dive into Python strings formatting on how to make our output to look nice. [Ultimately done that too](https://github.com/suankan/package_statistics/blob/master/package_statistics.py#L18-L33).

Overall this piece of work was done in about 24 hours with a lot of switching of context from one thing to another and trying to sneak it some time to work on it.

Ultimately I had a good time working on this project and I'm interested and opened to any comments/critics towards it.




