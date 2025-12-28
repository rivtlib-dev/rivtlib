# Release notes

<!-- do not remove -->

## 1.9.8

### New Features

- Add `pglob` and `fdelegates` ([#727](https://github.com/AnswerDotAI/fastcore/issues/727))

## 1.9.3

### New Features

- Add `unqid` ([#718](https://github.com/AnswerDotAI/fastcore/issues/718))


## 1.9.2

### Breaking Changes

- Patching a function no long clobbers a function with the same name in the current module

### New Features

- Have `@patch` not overwrite existing functions ([#717](https://github.com/AnswerDotAI/fastcore/issues/717))
- Add pre-3.11 support for `batched` ([#716](https://github.com/AnswerDotAI/fastcore/issues/716))
- Handle `nm` in `patch_to` and `patch` ([#715](https://github.com/AnswerDotAI/fastcore/issues/715))


## 1.8.18

### New Features

- Add more itertools etc to `L` ([#714](https://github.com/AnswerDotAI/fastcore/issues/714))

### Bugs Squashed

- missing import in `detect_mime` ([#712](https://github.com/AnswerDotAI/fastcore/issues/712))

## 1.8.15

### Bugs Squashed

- Incorrect json block in AttrDict ([#704](https://github.com/AnswerDotAI/fastcore/issues/704))


## 1.8.14

### New Features

- Add docments renderers (moved from nbdev) ([#703](https://github.com/AnswerDotAI/fastcore/issues/703))
- add `write_json` ([#702](https://github.com/AnswerDotAI/fastcore/pull/702)), thanks to [@RensDimmendaal](https://github.com/RensDimmendaal)


