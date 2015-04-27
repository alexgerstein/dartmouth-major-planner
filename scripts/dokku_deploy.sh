if ([ "$TRAVIS_PULL_REQUEST" == "false" ] && [ "$TRAVIS_BRANCH" == "production" ]); then
  git remote add dokku dokku@dartplan.com:dartplan
  git push dokku production
fi
