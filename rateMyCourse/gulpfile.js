var gulp = require('gulp');
var browserSync = require('browser-sync');
var htmlImport = require('gulp-html-import');

gulp.task('default', ['importIndexNavbar', 'importCommonNavbar']);

gulp.task('syncBrowser', function() {
  browserSync.init({
    proxy: "localhost:8000"
  });
  gulp.watch('templates/rateMyCourse/*.html', browserSync.reload);
  gulp.watch('templates/ratemycourse/javascript/*.js', browserSync.reload);
  gulp.watch('static/ratemycourse/css/*.css', browserSync.reload);
});

gulp.task('importIndexNavbar', function () {
    gulp.src('templates/rateMyCourse/templates/index.html')
        .pipe(htmlImport('templates/rateMyCourse/components/'))
        .pipe(gulp.dest('templates/rateMyCourse'))
})

gulp.task('importCommonNavbar', function () {
    gulp.src('templates/rateMyCourse/templates/searchResult.html')
        .pipe(htmlImport('templates/rateMyCourse/components/'))
        .pipe(gulp.dest('templates/rateMyCourse'))

    gulp.src('templates/rateMyCourse/templates/coursePage.html')
        .pipe(htmlImport('templates/rateMyCourse/components/'))
        .pipe(gulp.dest('templates/rateMyCourse'))

    gulp.src('templates/rateMyCourse/templates/ratePage.html')
        .pipe(htmlImport('templates/rateMyCourse/components/'))
        .pipe(gulp.dest('templates/rateMyCourse'))

    gulp.src('templates/rateMyCourse/templates/userPage.html')
        .pipe(htmlImport('templates/rateMyCourse/components/'))
        .pipe(gulp.dest('templates/rateMyCourse'))

    gulp.src('templates/rateMyCourse/templates/addRatePage.html')
        .pipe(htmlImport('templates/rateMyCourse/components/'))
        .pipe(gulp.dest('templates/rateMyCourse'))
})
