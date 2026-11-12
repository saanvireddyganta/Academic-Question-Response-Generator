FROM pytorch/torchserve:0.11.0-cpu
USER root
RUN pip install --no-cache-dir transformers==4.40.2 tokenizers==0.19.1
RUN mkdir -p /home/model-server/model-store
COPY torchserve/handler.py /home/model-server/handler.py
COPY torchserve/config.properties /home/model-server/config.properties
COPY torchserve/model_store/academic_generator.mar /home/model-server/model-store/academic_generator.mar
EXPOSE 8080 8081 8082
CMD ["torchserve","--start","--foreground","--model-store","/home/model-server/model-store","--models","academic_generator=academic_generator.mar","--ts-config","/home/model-server/config.properties"]
